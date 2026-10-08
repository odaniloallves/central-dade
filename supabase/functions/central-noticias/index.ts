// Notícias do dia para o Início da central: lê feeds RSS fixos de design e marketing e devolve JSON.
// Só lê a lista fixa abaixo; não aceita URL de fora.
const FEEDS = [
  { nome: 'B9', url: 'https://www.b9.com.br/feed/' },
  { nome: 'Meio & Mensagem', url: 'https://www.meioemensagem.com.br/feed' },
  { nome: 'Google Notícias', url: 'https://news.google.com/rss/search?q=design+OR+branding+OR+%22identidade+visual%22+when:2d&hl=pt-BR&gl=BR&ceid=BR:pt-419' },
];
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, apikey, content-type, x-client-info',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
};
let cache: { em: number; body: string } | null = null;

const ent = (s: string) => s
  .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
  .replace(/<[^>]+>/g, '')
  .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
  .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCharCode(parseInt(n, 16)))
  .replace(/&quot;/g, '"').replace(/&apos;|&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&')
  .replace(/\s+/g, ' ').trim();
const tag = (item: string, t: string) => { const m = item.match(new RegExp(`<${t}[^>]*>([\\s\\S]*?)</${t}>`, 'i')); return m ? ent(m[1]) : ''; };

async function ler(f: { nome: string; url: string }) {
  const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 6000);
  try {
    const r = await fetch(f.url, { signal: ctl.signal, headers: { 'User-Agent': 'Mozilla/5.0 (central dade)' } });
    if (!r.ok) return [];
    const xml = await r.text();
    return [...xml.matchAll(/<item[\s>][\s\S]*?<\/item>/gi)].slice(0, 15).map(([it]) => {
      let titulo = tag(it, 'title'), fonte = tag(it, 'source') || f.nome;
      if (f.nome === 'Google Notícias' && fonte && titulo.endsWith(' - ' + fonte)) titulo = titulo.slice(0, -(fonte.length + 3));
      const link = tag(it, 'link'), data = new Date(tag(it, 'pubDate') || Date.now()).toISOString();
      return { titulo, link, fonte, data };
    }).filter(n => n.titulo && /^https?:\/\//.test(n.link));
  } catch { return []; } finally { clearTimeout(t); }
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  if (!cache || Date.now() - cache.em > 30 * 60 * 1000) {
    const todas = (await Promise.all(FEEDS.map(ler))).flat();
    const vistos = new Set<string>();
    const itens = todas.sort((a, b) => b.data.localeCompare(a.data)).filter(n => { const k = n.titulo.toLowerCase().slice(0, 60); if (vistos.has(k)) return false; vistos.add(k); return true; }).slice(0, 12);
    const body = JSON.stringify({ itens, atualizado: new Date().toISOString() });
    if (itens.length) cache = { em: Date.now(), body }; else return new Response(body, { headers: { ...CORS, 'Content-Type': 'application/json' } });
  }
  return new Response(cache!.body, { headers: { ...CORS, 'Content-Type': 'application/json', 'Cache-Control': 'private, max-age=900' } });
});
