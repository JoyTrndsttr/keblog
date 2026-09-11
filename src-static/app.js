const page = document.body.dataset.page;
document.querySelector(`[data-nav="${page}"]`)?.classList.add('active');

const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-header nav');
navToggle?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
  navToggle.textContent = open ? '关闭' : '菜单';
});
nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
  nav.classList.remove('open');
  navToggle?.setAttribute('aria-expanded', 'false');
}));

const escapeHtml = (value) => value.replace(/[&<>"']/g, (char) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;',
}[char]));

function inline(text) {
  return escapeHtml(text)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+?)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+|\/[^\s)]*|\.\/[^\s)]*|#[^\s)]*)\)/g, (match, label, href) => {
      const external = /^https?:\/\//.test(href);
      return `<a href="${href}"${external ? ' target="_blank" rel="noreferrer"' : ''}>${label}</a>`;
    })
    .replace(/`([^`]+)`/g, '<code>$1</code>');
}

function markdownToHtml(markdown) {
  const lines = markdown.replace(/\r/g, '').split('\n');
  const html = [];
  let inTable = false;
  let listType = '';
  let inCode = false;
  const closeBlocks = () => {
    if (inTable) { html.push('</tbody></table></div>'); inTable = false; }
    if (listType) { html.push(`</${listType}>`); listType = ''; }
  };
  for (let index = 0; index < lines.length; index += 1) {
    const raw = lines[index];
    const line = raw.trim();
    if (line.startsWith('```')) {
      closeBlocks();
      if (inCode) { html.push('</code></pre>'); inCode = false; }
      else { html.push('<pre><code>'); inCode = true; }
      continue;
    }
    if (inCode) { html.push(`${escapeHtml(raw)}\n`); continue; }
    if (!line) { closeBlocks(); continue; }
    if (/^---+$/.test(line)) { closeBlocks(); html.push('<hr>'); continue; }
    if (/^\|.+\|$/.test(line)) {
      const cells = line.slice(1, -1).split('|').map((cell) => cell.trim());
      const next = lines[index + 1]?.trim() || '';
      if (!inTable) {
        closeBlocks();
        inTable = true;
        const isHeader = /^\|(?:\s*:?-+:?\s*\|)+$/.test(next);
        html.push('<div class="table-scroll"><table>');
        if (isHeader) {
          html.push(`<thead><tr>${cells.map((cell) => `<th>${inline(cell)}</th>`).join('')}</tr></thead><tbody>`);
          index += 1;
          continue;
        }
        html.push('<tbody>');
      }
      html.push(`<tr>${cells.map((cell) => `<td>${inline(cell)}</td>`).join('')}</tr>`);
      continue;
    }
    if (inTable) { html.push('</tbody></table></div>'); inTable = false; }
    const heading = /^(#{1,6})(?:\s+(.*?)|$)$/.exec(line);
    if (heading) {
      closeBlocks();
      const level = heading[1].length;
      const title = (heading[2] || '').replace(/(?:^|\s+)#+\s*$/, '');
      html.push(`<h${level}>${inline(title)}</h${level}>`);
    }
    else if (line.startsWith('> ')) { closeBlocks(); html.push(`<blockquote>${inline(line.slice(2))}</blockquote>`); }
    else if (/^- /.test(line)) {
      if (listType !== 'ul') { closeBlocks(); html.push('<ul>'); listType = 'ul'; }
      html.push(`<li>${inline(line.slice(2))}</li>`);
    } else if (/^\d+\.\s/.test(line)) {
      if (listType !== 'ol') { closeBlocks(); html.push('<ol>'); listType = 'ol'; }
      html.push(`<li>${inline(line.replace(/^\d+\.\s/, ''))}</li>`);
    } else {
      closeBlocks();
      html.push(`<p>${inline(line.replace(/ {2}$/, ''))}</p>`);
    }
  }
  if (inCode) html.push('</code></pre>');
  closeBlocks();
  return html.join('');
}

function updateStats(markdown, modified) {
  const read = (markdown.match(/\|\s*已精读(?:（[^）]+）)?\s*\|/g) || []).length;
  const candidateBlock = markdown.split('## 候选论文')[1]?.split('\n## ')[0] || '';
  const candidates = (candidateBlock.match(/^\|\s*\d{4}-\d{2}-\d{2}\s*\|/gm) || []).length;
  document.querySelectorAll('#read-count').forEach((node) => { node.textContent = String(read); });
  document.querySelectorAll('#candidate-count').forEach((node) => { node.textContent = String(candidates); });
  document.querySelectorAll('#updated-at').forEach((node) => { node.textContent = modified ? modified.slice(0, 10) : '—'; });
}

async function fetchPaperPool() {
  const response = await fetch('/api/documents/paperpool.md', { cache: 'no-store' });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function loadPaperPool() {
  const content = document.querySelector('#paperpool-content');
  const refresh = document.querySelector('#refresh-button');
  if (refresh) { refresh.disabled = true; refresh.textContent = '读取中…'; }
  try {
    const payload = await fetchPaperPool();
    updateStats(payload.content, payload.modified);
    if (content) content.innerHTML = markdownToHtml(payload.content);
  } catch (error) {
    if (content) content.innerHTML = '<p class="error">论文池暂时无法读取。请稍后刷新，或检查服务状态。</p>';
    document.querySelectorAll('#updated-at').forEach((node) => { node.textContent = '暂不可用'; });
  } finally {
    if (refresh) { refresh.disabled = false; refresh.textContent = '刷新文档'; }
  }
}

document.querySelector('#refresh-button')?.addEventListener('click', loadPaperPool);
if (document.querySelector('#paperpool-content') || document.querySelector('#read-count')) loadPaperPool();

async function loadResearchDocument() {
  const content = document.querySelector('#research-document');
  if (!content) return;
  content.innerHTML = '<p class="loading">正在加载研究记录…</p>';
  try {
    const response = await fetch('/api/research/document', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    content.innerHTML = markdownToHtml(payload.content);
    const headings = [...content.querySelectorAll('h2, h3, h4')];
    const toc = document.querySelector('#research-toc');
    headings.forEach((heading, index) => { heading.id = `research-section-${index + 1}`; });
    if (toc) {
      toc.innerHTML = headings.map((heading) => `<a class="toc-${heading.tagName.toLowerCase()}" href="#${heading.id}">${escapeHtml(heading.textContent)}</a>`).join('');
    }
    const updated = document.querySelector('#research-updated');
    if (updated) updated.textContent = `UPDATED ${payload.modified.slice(0, 10)}`;
  } catch (error) {
    content.innerHTML = '<p class="error">研究记录暂时无法读取，请稍后重试。</p>';
  }
}

if (document.querySelector('#research-document')) loadResearchDocument();

async function loadPublicationDetail() {
  const content = document.querySelector('#publication-detail');
  if (!content) return;
  try {
    const response = await fetch('./content.md', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    content.innerHTML = markdownToHtml(await response.text());
    const headings = [...content.querySelectorAll('h2, h3, h4')];
    headings.forEach((heading, index) => { heading.id = `publication-section-${index + 1}`; });
    const toc = document.querySelector('#publication-toc');
    if (toc) toc.innerHTML = headings.map((heading) => `<a class="toc-${heading.tagName.toLowerCase()}" href="#${heading.id}">${escapeHtml(heading.textContent)}</a>`).join('');
  } catch (error) {
    content.innerHTML = '<p class="error">论文介绍暂时无法读取，请稍后重试。</p>';
  }
}

if (document.querySelector('#publication-detail')) loadPublicationDetail();

let learningEntries = [];
async function fetchLearning(slug) {
  const response = await fetch(`/api/daily-learning/${encodeURIComponent(slug)}`, { cache: 'no-store' });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

function selectLearningLink(slug) {
  document.querySelectorAll('[data-learning-slug]').forEach((node) => {
    node.classList.toggle('active', node.dataset.learningSlug === slug);
  });
}

function decorateLearningDocument() {
  const content = document.querySelector('#learning-content');
  const toc = document.querySelector('#learning-toc');
  if (!content || !toc) return;
  const headings = [...content.querySelectorAll('h2, h3')];
  headings.forEach((heading, index) => { heading.id = `section-${index + 1}`; });
  toc.innerHTML = headings.map((heading) => `<a class="toc-${heading.tagName.toLowerCase()}" href="#${heading.id}">${escapeHtml(heading.textContent)}</a>`).join('');
  document.querySelector('.learning-toc').hidden = headings.length < 2;
}

function scrollToLearningHash(hash = location.hash, behavior = 'auto') {
  if (!hash.startsWith('#')) return false;
  const target = document.getElementById(decodeURIComponent(hash.slice(1)));
  if (!target) return false;
  target.scrollIntoView({ behavior, block: 'start' });
  return true;
}

function updateReadingProgress() {
  const bar = document.querySelector('#reading-progress-bar');
  if (!bar) return;
  const available = document.documentElement.scrollHeight - window.innerHeight;
  const progress = available > 0 ? Math.min(1, Math.max(0, window.scrollY / available)) : 0;
  bar.style.transform = `scaleX(${progress})`;
}

async function openLearning(slug, push = true) {
  const content = document.querySelector('#learning-content');
  if (!content) return;
  content.innerHTML = '<p class="loading">正在载入精读笔记…</p>';
  selectLearningLink(slug);
  try {
    const payload = await fetchLearning(slug);
    const entry = learningEntries.find((item) => item.slug === slug);
    const systemTitle = slug === 'plan' ? '每日任务执行规则' : '阅读计划与完成记录';
    document.querySelector('#learning-title').textContent = entry?.title || systemTitle;
    document.querySelector('#learning-date').textContent = entry ? `${entry.date} · ${entry.author}` : slug === 'plan' ? '08:30 · ASIA/SHANGHAI' : 'DAILY LEARNING INDEX';
    const doi = document.querySelector('#learning-doi');
    if (entry?.doi) { doi.href = `https://doi.org/${entry.doi}`; doi.hidden = false; } else { doi.hidden = true; }
    content.innerHTML = markdownToHtml(payload.content);
    decorateLearningDocument();
    if (push) history.pushState({ paper: slug }, '', `/daily-learning/?paper=${encodeURIComponent(slug)}`);
    const targetHash = push ? '' : location.hash;
    if (!targetHash) window.scrollTo({ top: 0, behavior: 'instant' });
    else requestAnimationFrame(() => requestAnimationFrame(() => scrollToLearningHash(targetHash)));
    updateReadingProgress();
  } catch (error) {
    content.innerHTML = '<p class="error">这篇精读笔记暂时无法读取，请稍后重试。</p>';
  }
}

async function loadDailyLearning() {
  const list = document.querySelector('#learning-list');
  if (!list) return;
  try {
    const response = await fetch('/api/daily-learning', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    learningEntries = payload.entries;
    document.querySelector('#learning-count').textContent = String(learningEntries.length);
    list.innerHTML = learningEntries.map((entry) => `
      <a href="/daily-learning/?paper=${encodeURIComponent(entry.slug)}" data-learning-slug="${entry.slug}">
        <time>${entry.date.replaceAll('-', '.')}</time>
        <b>${escapeHtml(entry.shortName)}</b>
        <span>${escapeHtml(entry.title)}</span>
      </a>`).join('') || '<p class="loading">还没有完成的精读。</p>';
    const selected = new URLSearchParams(location.search).get('paper');
    const initial = ['index', 'plan'].includes(selected) || learningEntries.some((entry) => entry.slug === selected)
      ? selected
      : (learningEntries[0]?.slug || 'index');
    openLearning(initial, false);
  } catch (error) {
    list.innerHTML = '<p class="error">精读索引暂时无法读取。</p>';
    document.querySelector('#learning-content').innerHTML = '<p class="error">每日学习服务暂时不可用。</p>';
  }
}

document.querySelector('.learning-shell')?.addEventListener('click', (event) => {
  const link = event.target.closest('a');
  if (!link) return;
  const hash = link.getAttribute('href');
  if (hash?.startsWith('#')) {
    event.preventDefault();
    history.pushState(history.state, '', hash);
    scrollToLearningHash(hash, 'smooth');
    return;
  }
  const directSlug = link.dataset.learningSlug;
  const markdownMatch = link.getAttribute('href')?.match(/^\.\/([^/]+)\/README\.md$/);
  const planMatch = link.getAttribute('href') === './PLAN.md';
  const slug = directSlug || markdownMatch?.[1] || (planMatch ? 'plan' : '');
  if (!slug) return;
  event.preventDefault();
  openLearning(slug);
});
window.addEventListener('popstate', () => {
  if (page === 'daily-learning') openLearning(new URLSearchParams(location.search).get('paper') || learningEntries[0]?.slug || 'index', false);
});
if (page === 'daily-learning') loadDailyLearning();

let readingScale = Number(localStorage.getItem('dailyLearningFontScale') || '1');
function applyReadingScale() {
  readingScale = Math.min(1.24, Math.max(.9, readingScale));
  document.querySelector('.learning-reader')?.style.setProperty('--reading-scale', String(readingScale));
  localStorage.setItem('dailyLearningFontScale', String(readingScale));
}
document.querySelectorAll('[data-reading-size]').forEach((button) => button.addEventListener('click', () => {
  const action = button.dataset.readingSize;
  readingScale = action === 'larger' ? readingScale + .08 : action === 'smaller' ? readingScale - .08 : 1;
  applyReadingScale();
}));
document.querySelector('#reading-width')?.addEventListener('click', (event) => {
  const reader = document.querySelector('.learning-reader');
  const wide = reader.classList.toggle('wide-reading');
  event.currentTarget.textContent = wide ? '窄栏' : '宽屏';
  localStorage.setItem('dailyLearningWide', String(wide));
});
if (page === 'daily-learning') {
  applyReadingScale();
  if (localStorage.getItem('dailyLearningWide') === 'true') {
    document.querySelector('.learning-reader')?.classList.add('wide-reading');
    document.querySelector('#reading-width').textContent = '窄栏';
  }
  window.addEventListener('scroll', updateReadingProgress, { passive: true });
}

const modelContext = document.modelContext;
if (modelContext?.registerTool) {
  const lifecycle = new AbortController();
  Promise.resolve(modelContext.registerTool({
    name: 'read_paper_pool',
    title: '读取每日论文池',
    description: '读取王柯的每日论文池，包括已精读论文、候选论文和最近维护时间。',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
    annotations: { readOnlyHint: true, untrustedContentHint: true },
    async execute() {
      const payload = await fetchPaperPool();
      return { name: payload.name, content: payload.content, modified: payload.modified, etag: payload.etag };
    },
  }, { signal: lifecycle.signal })).catch(() => {});
  Promise.resolve(modelContext.registerTool({
    name: 'read_daily_learning',
    title: '读取每日学习',
    description: '读取每日学习计划、索引或指定论文的精读 Markdown。',
    inputSchema: { type: 'object', properties: { slug: { type: 'string', description: '使用 plan、index 或论文目录名。' } }, required: ['slug'], additionalProperties: false },
    annotations: { readOnlyHint: true, untrustedContentHint: true },
    async execute({ slug }) { return fetchLearning(slug); },
  }, { signal: lifecycle.signal })).catch(() => {});
}
