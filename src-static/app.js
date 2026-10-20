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
  const listStack = [];
  let inCode = false;
  const closeList = () => {
    while (listStack.length) {
      const { type, liOpen } = listStack.pop();
      if (liOpen) html.push('</li>');
      html.push(`</${type}>`);
    }
  };
  const closeBlocks = () => {
    if (inTable) { html.push('</tbody></table></div>'); inTable = false; }
    closeList();
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
    if (line === '\\[' || line === '$$') {
      closeBlocks();
      const closing = line === '$$' ? '$$' : '\\]';
      const formula = [];
      while (index + 1 < lines.length && lines[index + 1].trim() !== closing) {
        formula.push(lines[++index]);
      }
      if (index + 1 < lines.length) index += 1;
      html.push(`<div class="math-block" data-tex="${escapeHtml(formula.join('\n'))}"></div>`);
      continue;
    }
    if (!line) {
      const next = lines.slice(index + 1).find((item) => item.trim());
      if (!listStack.length || !next || !/^\s*(?:- |\d+\.\s)/.test(next)) closeBlocks();
      continue;
    }
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
    else if (/^(?:- |\d+\.\s)/.test(line)) {
      const type = line.startsWith('- ') ? 'ul' : 'ol';
      const indent = raw.match(/^\s*/)[0].length;
      while (listStack.length && indent < listStack.at(-1).indent) {
        const previous = listStack.pop();
        if (previous.liOpen) html.push('</li>');
        html.push(`</${previous.type}>`);
      }
      if (listStack.length && indent === listStack.at(-1).indent && listStack.at(-1).type !== type) {
        const previous = listStack.pop();
        if (previous.liOpen) html.push('</li>');
        html.push(`</${previous.type}>`);
      }
      if (!listStack.length || indent > listStack.at(-1).indent) {
        html.push(`<${type}>`);
        listStack.push({ type, indent, liOpen: false });
      }
      const current = listStack.at(-1);
      if (current.liOpen) html.push('</li>');
      html.push(`<li>${inline(line.replace(/^(?:- |\d+\.\s)/, ''))}`);
      current.liOpen = true;
    } else {
      closeBlocks();
      html.push(`<p>${inline(line.replace(/ {2}$/, ''))}</p>`);
    }
  }
  if (inCode) html.push('</code></pre>');
  closeBlocks();
  return html.join('');
}

function renderMathematics(element) {
  if (!element || !window.katex || !window.renderMathInElement) return;
  element.querySelectorAll('.math-block').forEach((block) => {
    window.katex.render(block.dataset.tex, block, { displayMode: true, throwOnError: false, trust: false });
  });
  window.renderMathInElement(element, {
    delimiters: [
      { left: '$$', right: '$$', display: true },
      { left: '\\[', right: '\\]', display: true },
      { left: '\\(', right: '\\)', display: false },
      { left: '$', right: '$', display: false },
    ],
    ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
    throwOnError: false,
    trust: false,
  });
}

function renderPaperPoolMonths(content) {
  if (!content) return;
  const children = [...content.children];
  const datedHeadings = children.filter((node) => node.tagName === 'H3' && /^\d{4}-\d{2}-\d{2}$/.test(node.textContent.trim()));
  if (!datedHeadings.length) return;
  const firstDateIndex = children.indexOf(datedHeadings[0]);
  const prefix = children.slice(0, firstDateIndex);
  const months = new Map();
  const tail = [];
  let current = null;
  let inTail = false;
  for (const node of children.slice(firstDateIndex)) {
    const dateHeading = node.tagName === 'H3' && /^\d{4}-\d{2}-\d{2}$/.test(node.textContent.trim());
    if (dateHeading) {
      const month = node.textContent.trim().slice(0, 7);
      current = months.get(month) || { month, nodes: [], count: 0 };
      months.set(month, current);
      current.count += 1;
      inTail = false;
    }
    if (node.tagName === 'H2' && /待精读/.test(node.textContent)) inTail = true;
    if (inTail) {
      inTail = true;
      tail.push(node);
    } else if (current) {
      current.nodes.push(node);
    }
  }
  if (!months.size) return;
  const monthNav = document.createElement('nav');
  monthNav.className = 'paperpool-month-nav';
  monthNav.setAttribute('aria-label', '按月份查看论文池');
  const monthSections = document.createElement('div');
  monthSections.className = 'paperpool-month-sections';
  const monthLabel = (month) => `${month.slice(0, 4)}年${month.slice(5)}月`;
  const monthEntries = [...months.values()].sort((a, b) => b.month.localeCompare(a.month));
  monthEntries.forEach((item, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.dataset.paperpoolMonth = item.month;
    button.setAttribute('aria-pressed', String(index === 0));
    button.innerHTML = `<b>${monthLabel(item.month)}</b><span>${item.count} 个日期</span>`;
    monthNav.append(button);

    const section = document.createElement('section');
    section.className = 'paperpool-month';
    section.dataset.paperpoolMonth = item.month;
    section.hidden = index !== 0;
    const heading = document.createElement('h3');
    heading.className = 'paperpool-month-title';
    heading.innerHTML = `<span>${monthLabel(item.month)}</span><small>${item.count} 个精读日期</small>`;
    section.append(heading, ...item.nodes);
    monthSections.append(section);
  });
  monthNav.addEventListener('click', (event) => {
    const button = event.target.closest('[data-paperpool-month]');
    if (!button) return;
    const selected = button.dataset.paperpoolMonth;
    monthNav.querySelectorAll('[data-paperpool-month]').forEach((node) => node.setAttribute('aria-pressed', String(node === button)));
    monthSections.querySelectorAll('[data-paperpool-month]').forEach((node) => { node.hidden = node.dataset.paperpoolMonth !== selected; });
  });
  content.replaceChildren(...prefix, monthNav, monthSections, ...tail);
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
  const payload = await response.json();
  payload.content = payload.content.replace(/^> \*\*维护约定\*\*\n(?:>[^\n]*\n)*/m, '');
  const monthlyFiles = [...payload.content.matchAll(/`(paperpool_\d{6}\.md)`/g)].map((match) => match[1]);
  if (monthlyFiles.length) {
    const documents = await Promise.all(monthlyFiles.map(async (name) => {
      const monthlyResponse = await fetch(`/api/documents/${encodeURIComponent(name)}`, { cache: 'no-store' });
      if (!monthlyResponse.ok) throw new Error(`HTTP ${monthlyResponse.status}`);
      return monthlyResponse.json();
    }));
    payload.content = documents.map((document) => document.content.split('\n## 已精读论文', 2)[1] || document.content).join('\n\n');
  }
  return payload;
}

async function loadPaperPool() {
  const content = document.querySelector('#paperpool-content');
  const refresh = document.querySelector('#refresh-button');
  if (refresh) { refresh.disabled = true; refresh.textContent = '读取中…'; }
  try {
    const payload = await fetchPaperPool();
    updateStats(payload.content, payload.modified);
    if (content) { content.innerHTML = markdownToHtml(payload.content); renderMathematics(content); }
  } catch (error) {
    if (content) content.innerHTML = '<p class="error">论文池暂时无法读取。请稍后刷新，或检查服务状态。</p>';
    document.querySelectorAll('#updated-at').forEach((node) => { node.textContent = '暂不可用'; });
  } finally {
    if (refresh) { refresh.disabled = false; refresh.textContent = '刷新文档'; }
  }
}

document.querySelector('#refresh-button')?.addEventListener('click', loadPaperPool);
if (document.querySelector('#paperpool-content')) loadPaperPool();
if (document.querySelector('#home-learning-count')) {
  fetch('/api/daily-learning', { cache: 'no-store' })
    .then((response) => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); })
    .then((payload) => { document.querySelector('#home-learning-count').innerHTML = `${payload.entries.length}<span>篇</span>`; })
    .catch(() => { document.querySelector('#home-learning-count').innerHTML = '—<span>篇</span>'; });
}

async function loadResearchDocument() {
  const content = document.querySelector('#research-document');
  if (!content) return;
  content.innerHTML = '<p class="loading">正在加载研究记录…</p>';
  try {
    const response = await fetch('/api/research/document', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    content.innerHTML = markdownToHtml(payload.content);
    renderMathematics(content);
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
    renderMathematics(content);
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
const learningTags = new Set();
let learningSearchOpen = false;

function parsePaperPoolIndex(markdown) {
  const details = new Map();
  let current = null;
  for (const line of markdown.split('\n')) {
    const short = line.match(/^\s+- 简称：\[([^\]]+)\]\([^)]*[?&]paper=([^&#)]+)[^)]*\)/);
    if (short) {
      current = decodeURIComponent(short[2]);
      details.set(current, { displayName: short[1], tags: [] });
      continue;
    }
    const tags = line.match(/^\s+- Tags：(.+)$/);
    if (tags && current) {
      details.get(current).tags = [...tags[1].matchAll(/`([^`]+)`/g)].map((match) => match[1]);
      current = null;
    }
  }
  return details;
}

function normalized(value) {
  return String(value).normalize('NFKC').toLocaleLowerCase().trim();
}

function fuzzyScore(value, query) {
  const text = normalized(value);
  const wanted = normalized(query);
  if (!wanted) return 0;
  const position = text.indexOf(wanted);
  if (position >= 0) return 100 - Math.min(position, 50);
  let cursor = 0;
  let gaps = 0;
  for (const letter of wanted) {
    const found = text.indexOf(letter, cursor);
    if (found < 0) return -1;
    gaps += found - cursor;
    cursor = found + 1;
  }
  return 30 - Math.min(gaps, 25);
}

function findLearningEntries(query = '', tags = learningTags) {
  const terms = normalized(query).split(/\s+/).filter(Boolean);
  return learningEntries
    .filter((entry) => [...tags].every((tag) => entry.tags.includes(tag)))
    .map((entry) => {
      let score = 0;
      for (const term of terms) {
        const weighted = (value, bonus = 0) => {
          const match = fuzzyScore(value, term);
          return match < 0 ? -1 : match + bonus;
        };
        const best = Math.max(
          weighted(entry.displayName, 20),
          weighted(entry.shortName, 10),
          weighted(entry.title),
          weighted(entry.author),
          ...entry.tags.map((item) => weighted(item)),
        );
        if (best < 0) return null;
        score += best;
      }
      return { entry, score };
    })
    .filter(Boolean)
    .sort((a, b) => b.score - a.score || b.entry.date.localeCompare(a.entry.date))
    .map((item) => item.entry);
}

function learningResultLink(entry, compact = false) {
  return `<a href="/daily-learning/?paper=${encodeURIComponent(entry.slug)}" data-learning-slug="${entry.slug}">
    <span><b>${escapeHtml(entry.displayName)}</b>${compact ? '' : `<small>${escapeHtml(entry.title)}</small>`}</span>
    <time>${escapeHtml(entry.date)}</time>
  </a>`;
}

function renderLearningSearch() {
  const panel = document.querySelector('#learning-search-results');
  const input = document.querySelector('#learning-search');
  if (!panel || !input) return;
  panel.hidden = !learningSearchOpen && !learningTags.size && !input.value.trim();
  if (panel.hidden) return;
  const matches = findLearningEntries(input.value);
  panel.innerHTML = `<div class="learning-result-caption">${learningTags.size ? `已选 ${learningTags.size} 个标签` : input.value.trim() ? '搜索结果' : '快速建议'}<span>${matches.length} 篇</span></div>`
    + (matches.slice(0, 5).map((entry) => learningResultLink(entry)).join('') || '<p class="learning-empty">没有匹配的论文</p>')
    + (matches.length > 5 ? `<button class="learning-more-results" type="button">查看全部 ${matches.length} 篇 →</button>` : '');
}

function renderLearningDialog() {
  const input = document.querySelector('#learning-dialog-search');
  const list = document.querySelector('#learning-dialog-list');
  if (!input || !list) return;
  const matches = findLearningEntries(input.value);
  document.querySelector('#learning-dialog-count').textContent = `${matches.length} / ${learningEntries.length} 篇`;
  list.innerHTML = matches.map((entry) => learningResultLink(entry)).join('') || '<p class="learning-empty">没有匹配的论文</p>';
}

function showAllLearning() {
  const dialog = document.querySelector('#learning-all-dialog');
  document.querySelector('#learning-dialog-search').value = document.querySelector('#learning-search').value;
  renderLearningDialog();
  if (!dialog.open) dialog.showModal();
}

function renderLearningNavigation() {
  document.querySelector('#learning-count').textContent = String(learningEntries.length);
  const list = document.querySelector('#learning-list');
  list.innerHTML = learningEntries.slice(0, 3).map((entry) => `
    <a href="/daily-learning/?paper=${encodeURIComponent(entry.slug)}" data-learning-slug="${entry.slug}">
      <time>${escapeHtml(entry.date.slice(5).replace('-', '.'))}</time><b>${escapeHtml(entry.displayName)}</b>
    </a>`).join('') || '<p class="loading">还没有完成的精读。</p>';
  const shortcuts = learningEntries.slice(0, 30);
  const shortcutList = document.querySelector('#learning-shortcuts');
  shortcutList.style.setProperty('--shortcut-rows', String(Math.min(10, shortcuts.length)));
  shortcutList.innerHTML = shortcuts.map((entry) => `<a href="/daily-learning/?paper=${encodeURIComponent(entry.slug)}" data-learning-slug="${escapeHtml(entry.slug)}" title="${escapeHtml(entry.displayName)}"><b>${escapeHtml(entry.displayName)}</b></a>`).join('');
  const counts = new Map();
  learningEntries.forEach((entry) => entry.tags.forEach((tag) => counts.set(tag, (counts.get(tag) || 0) + 1)));
  const tags = [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'zh-CN'));
  document.querySelector('#learning-tags').innerHTML = tags.map(([tag, count]) => `<button type="button" data-learning-tag="${escapeHtml(tag)}" aria-pressed="false">${escapeHtml(tag)}<span>${count}</span></button>`).join('') || '<p class="learning-empty">标签暂时不可用</p>';
}

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

let currentUser = null;
let activeCommunitySlug = '';
let activeCommunity = null;
let communityRequestId = 0;
let pendingSelection = null;
let authMode = 'login';

function formatCommunityDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) return value || '';
  return date.toLocaleString('zh-CN', { dateStyle: 'medium', timeStyle: 'short' });
}

function communityErrorMessage(payload, fallback = '操作暂时无法完成，请稍后重试。') {
  return payload?.message || fallback;
}

function renderAccountWidget() {
  const widget = document.querySelector('#account-widget');
  if (!widget) return;
  if (currentUser) {
    widget.innerHTML = `<span class="account-user">${escapeHtml(currentUser.displayName)}</span><button type="button" class="account-logout" data-auth-action="logout">退出</button>`;
  } else {
    widget.innerHTML = '<button type="button" class="account-button" data-auth-action="login">登录</button>';
  }
}

function setAuthMode(mode) {
  authMode = mode === 'register' ? 'register' : 'login';
  const register = authMode === 'register';
  document.querySelectorAll('[data-auth-mode]').forEach((button) => button.setAttribute('aria-selected', String(button.dataset.authMode === authMode)));
  const title = document.querySelector('#auth-dialog-title');
  const submit = document.querySelector('#auth-submit');
  const displayLabel = document.querySelector('#auth-display-label');
  const password = document.querySelector('#auth-password');
  if (title) title.textContent = register ? '注册后参与讨论' : '登录后参与讨论';
  if (submit) submit.textContent = register ? '注册并登录' : '登录';
  if (displayLabel) displayLabel.hidden = !register;
  if (displayLabel) displayLabel.querySelector('input').required = register;
  if (password) password.autocomplete = register ? 'new-password' : 'current-password';
  const error = document.querySelector('#auth-error');
  if (error) error.textContent = '';
}

function openAuth(mode = 'login') {
  const dialog = document.querySelector('#auth-dialog');
  if (!dialog) return;
  setAuthMode(mode);
  if (!dialog.open) dialog.showModal();
  document.querySelector('#auth-username')?.focus();
}

async function fetchCurrentUser() {
  try {
    const response = await fetch('/api/auth/me', { cache: 'no-store', credentials: 'same-origin' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    currentUser = (await response.json()).user;
  } catch (error) {
    currentUser = null;
  }
  renderAccountWidget();
}

function statusLabel(status) {
  return ({ unread: '待阅读', read: '已阅读', deeper: '待深入' })[status] || '待阅读';
}

function renderCommunity(payload) {
  const community = document.querySelector('#reader-community');
  if (!community) return;
  activeCommunity = payload;
  const selectedStatus = payload.status || 'unread';
  const statusButtons = ['unread', 'read', 'deeper'].map((status) => `<button type="button" data-reading-status="${status}" aria-pressed="${selectedStatus === status}">${statusLabel(status)}</button>`).join('');
  const noteCards = payload.notes.map((note) => `<article class="community-note-card" data-note-card="${note.id}"><p class="community-note-quote">${escapeHtml(note.quote)}</p><p class="community-note-content">${escapeHtml(note.content)}</p><div class="community-meta"><b>${escapeHtml(note.user.displayName)}</b><time>${escapeHtml(formatCommunityDate(note.createdAt))}</time></div></article>`).join('');
  const commentCards = payload.comments.map((comment) => `<article class="community-comment-card"><p class="community-comment-content">${escapeHtml(comment.content)}</p><div class="community-meta"><b>${escapeHtml(comment.user.displayName)}</b><time>${escapeHtml(formatCommunityDate(comment.createdAt))}</time></div></article>`).join('');
  const loginHint = '<button type="button" class="community-login-link" data-auth-action="login">登录后记录阅读状态</button>';
  const noteHint = currentUser ? '选中正文中的一段文字，再点击出现的“添加笔记”按钮。' : '选中正文中的一段文字即可查看划线入口；保存笔记需要登录。';
  const commentForm = currentUser
    ? '<form id="community-comment-form" class="community-form"><label for="community-comment-text">发表评论</label><textarea id="community-comment-text" rows="4" maxlength="5000" placeholder="分享你的理解、问题或补充" required></textarea><p id="community-comment-error" class="community-error" role="alert"></p><button class="button primary" type="submit">发布评论</button></form>'
    : '<p class="community-note-hint">文章公开阅读；<button type="button" class="community-login-link" data-auth-action="login">登录后发表评论</button></p>';
  community.innerHTML = `
    <section class="community-block community-status-block">
      <div class="community-heading"><h3>阅读状态</h3><span>${currentUser ? `已登录 · ${escapeHtml(currentUser.displayName)}` : 'PUBLIC READING'}</span></div>
      <div class="community-status-card"><p>${currentUser ? '为这篇精读设置你的下一步。当前：' + statusLabel(selectedStatus) : '正常阅读无需登录；登录后可以保存你的阅读进度。'}${currentUser ? '' : ` ${loginHint}`}</p><div class="community-status-actions">${statusButtons}</div></div>
    </section>
    <section class="community-block community-notes-block">
      <div class="community-heading"><h3>划线笔记</h3><span>${payload.notes.length} 条 · 按时间</span></div>
      <p class="community-note-hint">${noteHint}</p>
      <div class="community-notes-list" id="community-notes-list">${noteCards || '<p class="community-empty">还没有公开笔记。选中正文开始记录第一条。</p>'}</div>
    </section>
    <section class="community-block community-comments-block">
      <div class="community-heading"><h3>评论</h3><span>${payload.comments.length} 条 · 按时间</span></div>
      <div class="community-comments-list">${commentCards || '<p class="community-empty">还没有评论。</p>'}</div>
      ${commentForm}
    </section>`;
  community.hidden = false;
}

function textNodes(root) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      return node.parentElement?.closest('script,style') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
    },
  });
  const nodes = [];
  let node;
  while ((node = walker.nextNode())) nodes.push(node);
  return nodes;
}

function rangeAtOffsets(root, start, end) {
  if (!Number.isInteger(start) || !Number.isInteger(end) || start < 0 || end <= start) return null;
  let position = 0;
  let startNode = null;
  let endNode = null;
  let startOffset = 0;
  let endOffset = 0;
  for (const node of textNodes(root)) {
    const next = position + node.nodeValue.length;
    if (!startNode && start >= position && start <= next) {
      startNode = node;
      startOffset = start - position;
    }
    if (end >= position && end <= next) {
      endNode = node;
      endOffset = end - position;
      break;
    }
    position = next;
  }
  if (!startNode || !endNode) return null;
  const range = document.createRange();
  range.setStart(startNode, Math.max(0, startOffset));
  range.setEnd(endNode, Math.max(0, endOffset));
  return range;
}

function clearNoteHighlights() {
  document.querySelectorAll('#learning-content mark.reading-note-highlight').forEach((mark) => {
    mark.replaceWith(...mark.childNodes);
  });
}

function applyNoteHighlights(notes) {
  const content = document.querySelector('#learning-content');
  if (!content) return;
  clearNoteHighlights();
  [...notes].sort((a, b) => b.start - a.start).forEach((note) => {
    const range = rangeAtOffsets(content, note.start, note.end);
    if (!range || range.collapsed) return;
    const mark = document.createElement('mark');
    mark.className = 'reading-note-highlight';
    mark.dataset.noteId = String(note.id);
    try {
      mark.appendChild(range.extractContents());
      range.insertNode(mark);
    } catch (error) {
      // A changed Markdown document can invalidate an old range; keep its note visible in the list.
    }
  });
}

function focusCommunityNote(noteId) {
  const card = document.querySelector(`[data-note-card="${CSS.escape(String(noteId))}"]`);
  if (!card) return;
  card.classList.add('is-focused');
  card.scrollIntoView({ behavior: 'smooth', block: 'center' });
  window.setTimeout(() => card.classList.remove('is-focused'), 1800);
}

function selectionOffsets(root, range) {
  const startRange = range.cloneRange();
  startRange.selectNodeContents(root);
  startRange.setEnd(range.startContainer, range.startOffset);
  const endRange = range.cloneRange();
  endRange.selectNodeContents(root);
  endRange.setEnd(range.endContainer, range.endOffset);
  return { start: startRange.toString().length, end: endRange.toString().length };
}

function selectionPopover() {
  let popover = document.querySelector('#note-selection-popover');
  if (!popover) {
    popover = document.createElement('div');
    popover.id = 'note-selection-popover';
    popover.className = 'note-selection-popover';
    popover.hidden = true;
    popover.innerHTML = '<button type="button" data-note-action="open">添加笔记</button>';
    document.body.append(popover);
  }
  return popover;
}

function captureSelection() {
  const content = document.querySelector('#learning-content');
  const selection = window.getSelection();
  if (!content || !selection || selection.rangeCount === 0 || selection.isCollapsed) return;
  const range = selection.getRangeAt(0);
  if (!content.contains(range.commonAncestorContainer)) return;
  const rawQuote = selection.toString();
  const quote = rawQuote.trim();
  if (!quote || quote.length > 2000) return;
  const offsets = selectionOffsets(content, range);
  const leading = rawQuote.length - rawQuote.trimStart().length;
  pendingSelection = { quote, start: offsets.start + leading, end: offsets.start + leading + quote.length };
  const popover = selectionPopover();
  const rect = range.getBoundingClientRect();
  popover.hidden = false;
  popover.style.left = `${Math.max(12, Math.min(window.innerWidth - popover.offsetWidth - 12, rect.left + rect.width / 2 - popover.offsetWidth / 2))}px`;
  popover.style.top = `${Math.max(12, rect.top - popover.offsetHeight - 8)}px`;
}

function openNoteDialog() {
  if (!pendingSelection) return;
  const popover = document.querySelector('#note-selection-popover');
  if (popover) popover.hidden = true;
  if (!currentUser) {
    openAuth('login');
    return;
  }
  const dialog = document.querySelector('#note-dialog');
  document.querySelector('#note-selection-quote').textContent = pendingSelection.quote;
  document.querySelector('#note-text').value = '';
  document.querySelector('#note-error').textContent = '';
  if (dialog && !dialog.open) dialog.showModal();
  document.querySelector('#note-text')?.focus();
}

async function loadCommunity(slug) {
  const community = document.querySelector('#reader-community');
  if (!community) return;
  activeCommunitySlug = slug || '';
  const requestId = ++communityRequestId;
  if (!learningEntries.some((entry) => entry.slug === slug)) {
    activeCommunity = null;
    community.hidden = true;
    clearNoteHighlights();
    return;
  }
  community.hidden = false;
  community.innerHTML = '<p class="loading">正在读取评论和笔记…</p>';
  try {
    const response = await fetch(`/api/articles/${encodeURIComponent(slug)}/community`, { cache: 'no-store', credentials: 'same-origin' });
    const payload = await response.json();
    if (!response.ok) throw new Error(communityErrorMessage(payload));
    if (requestId !== communityRequestId) return;
    currentUser = payload.user;
    renderAccountWidget();
    renderCommunity(payload);
    applyNoteHighlights(payload.notes || []);
  } catch (error) {
    if (requestId === communityRequestId) community.innerHTML = '<p class="error">互动内容暂时无法读取，正文仍可正常阅读。</p>';
  }
}

async function submitCommunityComment(form) {
  const error = document.querySelector('#community-comment-error');
  const textarea = document.querySelector('#community-comment-text');
  if (!textarea || !activeCommunitySlug) return;
  error.textContent = '';
  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  try {
    const response = await fetch(`/api/articles/${encodeURIComponent(activeCommunitySlug)}/comments`, {
      method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: textarea.value }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(communityErrorMessage(payload));
    form.reset();
    await loadCommunity(activeCommunitySlug);
  } catch (errorValue) {
    error.textContent = errorValue.message;
  } finally {
    button.disabled = false;
  }
}

async function saveReadingStatus(status) {
  if (!currentUser) {
    openAuth('login');
    return;
  }
  try {
    const response = await fetch(`/api/articles/${encodeURIComponent(activeCommunitySlug)}/status`, {
      method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(communityErrorMessage(payload));
    if (activeCommunity) activeCommunity.status = status;
    renderCommunity(activeCommunity);
    applyNoteHighlights(activeCommunity.notes || []);
  } catch (error) {
    window.alert(error.message);
  }
}

document.querySelector('#learning-content')?.addEventListener('mouseup', captureSelection);
document.querySelector('#learning-content')?.addEventListener('keyup', captureSelection);
document.querySelector('#learning-content')?.addEventListener('click', (event) => {
  const mark = event.target.closest('.reading-note-highlight');
  if (mark) focusCommunityNote(mark.dataset.noteId);
});
document.querySelector('#reader-community')?.addEventListener('click', (event) => {
  const authAction = event.target.closest('[data-auth-action]')?.dataset.authAction;
  if (authAction === 'login') openAuth('login');
  if (authAction === 'logout') {
    fetch('/api/auth/logout', { method: 'POST', credentials: 'same-origin' }).finally(() => {
      currentUser = null;
      renderAccountWidget();
      if (activeCommunitySlug) loadCommunity(activeCommunitySlug);
    });
    return;
  }
  const statusButton = event.target.closest('[data-reading-status]');
  if (statusButton) saveReadingStatus(statusButton.dataset.readingStatus);
  const noteCard = event.target.closest('[data-note-card]');
  if (noteCard) {
    const mark = document.querySelector(`.reading-note-highlight[data-note-id="${CSS.escape(noteCard.dataset.noteCard)}"]`);
    mark?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
});
document.querySelector('#reader-community')?.addEventListener('submit', (event) => {
  if (event.target.id !== 'community-comment-form') return;
  event.preventDefault();
  submitCommunityComment(event.target);
});
document.addEventListener('click', (event) => {
  if (event.target.closest('[data-note-action="open"]')) openNoteDialog();
  const authAction = event.target.closest('#account-widget [data-auth-action]')?.dataset.authAction;
  if (authAction === 'login') openAuth('login');
  if (authAction === 'logout') {
    fetch('/api/auth/logout', { method: 'POST', credentials: 'same-origin' }).finally(() => {
      currentUser = null;
      renderAccountWidget();
      if (activeCommunitySlug) loadCommunity(activeCommunitySlug);
    });
  }
});
document.querySelectorAll('[data-auth-mode]').forEach((button) => button.addEventListener('click', () => setAuthMode(button.dataset.authMode)));
document.querySelector('#auth-close')?.addEventListener('click', () => document.querySelector('#auth-dialog').close());
document.querySelector('#note-close')?.addEventListener('click', () => document.querySelector('#note-dialog').close());
document.querySelector('#auth-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const error = document.querySelector('#auth-error');
  const button = document.querySelector('#auth-submit');
  error.textContent = '';
  button.disabled = true;
  const payload = {
    username: document.querySelector('#auth-username').value,
    password: document.querySelector('#auth-password').value,
    displayName: document.querySelector('#auth-display').value,
  };
  try {
    const response = await fetch(`/api/auth/${authMode}`, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const result = await response.json();
    if (!response.ok) throw new Error(communityErrorMessage(result));
    currentUser = result.user;
    renderAccountWidget();
    document.querySelector('#auth-dialog').close();
    if (activeCommunitySlug) await loadCommunity(activeCommunitySlug);
    if (pendingSelection && currentUser) openNoteDialog();
  } catch (errorValue) {
    error.textContent = errorValue.message;
  } finally {
    button.disabled = false;
  }
});
document.querySelector('#note-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!pendingSelection || !activeCommunitySlug) return;
  const error = document.querySelector('#note-error');
  const button = event.target.querySelector('button[type="submit"]');
  error.textContent = '';
  button.disabled = true;
  try {
    const response = await fetch(`/api/articles/${encodeURIComponent(activeCommunitySlug)}/notes`, {
      method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...pendingSelection, content: document.querySelector('#note-text').value }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(communityErrorMessage(result));
    document.querySelector('#note-dialog').close();
    pendingSelection = null;
    await loadCommunity(activeCommunitySlug);
  } catch (errorValue) {
    error.textContent = errorValue.message;
  } finally {
    button.disabled = false;
  }
});
document.querySelector('#account-widget')?.addEventListener('click', (event) => {
  const action = event.target.closest('[data-auth-action]')?.dataset.authAction;
  if (action === 'login') openAuth('login');
});
window.addEventListener('scroll', () => {
  const popover = document.querySelector('#note-selection-popover');
  if (popover) popover.hidden = true;
}, { passive: true });
renderAccountWidget();
if (page === 'daily-learning') fetchCurrentUser();

async function openLearning(slug, push = true) {
  const content = document.querySelector('#learning-content');
  if (!content) return;
  content.innerHTML = '<p class="loading">正在载入精读笔记…</p>';
  selectLearningLink(slug);
  try {
    const payload = slug === 'pool' ? await fetchPaperPool() : await fetchLearning(slug);
    const entry = learningEntries.find((item) => item.slug === slug);
    const systemTitle = slug === 'plan' ? '每日任务执行规则' : slug === 'pool' ? '候选论文与已读记录' : '阅读计划与完成记录';
    document.querySelector('#learning-title').textContent = entry?.title || systemTitle;
    document.querySelector('#learning-date').textContent = entry ? `${entry.date} · ${entry.author}` : slug === 'plan' ? '08:30 · ASIA/SHANGHAI' : slug === 'pool' ? 'PAPER POOL' : 'DAILY LEARNING INDEX';
    const doi = document.querySelector('#learning-doi');
    if (entry?.doi) { doi.href = `https://doi.org/${entry.doi}`; doi.hidden = false; } else { doi.hidden = true; }
    content.innerHTML = markdownToHtml(payload.content);
    renderMathematics(content);
    if (slug === 'pool') renderPaperPoolMonths(content);
    decorateLearningDocument();
    if (push) history.pushState({ paper: slug }, '', `/daily-learning/?paper=${encodeURIComponent(slug)}`);
    const targetHash = push ? '' : location.hash;
    if (!targetHash) window.scrollTo({ top: 0, behavior: 'instant' });
    else requestAnimationFrame(() => requestAnimationFrame(() => scrollToLearningHash(targetHash)));
    updateReadingProgress();
    if (entry) loadCommunity(slug);
    else {
      activeCommunitySlug = '';
      document.querySelector('#reader-community')?.setAttribute('hidden', '');
      clearNoteHighlights();
    }
  } catch (error) {
    content.innerHTML = '<p class="error">内容暂时无法读取，请稍后重试。</p>';
  }
}

async function loadDailyLearning() {
  const list = document.querySelector('#learning-list');
  if (!list) return;
  try {
    const [response, pool] = await Promise.all([
      fetch('/api/daily-learning', { cache: 'no-store' }),
      fetchPaperPool().catch(() => null),
    ]);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const details = parsePaperPoolIndex(pool?.content || '');
    learningEntries = (await response.json()).entries.map((entry) => ({
      ...entry,
      displayName: details.get(entry.slug)?.displayName || entry.shortName,
      tags: details.get(entry.slug)?.tags || [],
    }));
    renderLearningNavigation();
    const selected = new URLSearchParams(location.search).get('paper');
    const initial = ['index', 'plan', 'pool'].includes(selected) || learningEntries.some((entry) => entry.slug === selected)
      ? selected
      : (learningEntries[0]?.slug || 'index');
    openLearning(initial, false);
  } catch (error) {
    list.innerHTML = '<p class="error">精读索引暂时无法读取。</p>';
    document.querySelector('#learning-content').innerHTML = '<p class="error">每日学习服务暂时不可用。</p>';
  }
}

const learningSearch = document.querySelector('#learning-search');
learningSearch?.addEventListener('focus', () => { learningSearchOpen = true; renderLearningSearch(); });
learningSearch?.addEventListener('input', renderLearningSearch);
document.querySelector('#learning-search-results')?.addEventListener('click', (event) => {
  if (event.target.closest('.learning-more-results')) showAllLearning();
});
document.querySelector('#learning-show-all')?.addEventListener('click', showAllLearning);
document.querySelector('#learning-close-all')?.addEventListener('click', () => document.querySelector('#learning-all-dialog').close());
document.querySelector('#learning-dialog-search')?.addEventListener('input', renderLearningDialog);
document.querySelector('#learning-tags')?.addEventListener('click', (event) => {
  const button = event.target.closest('[data-learning-tag]');
  if (!button) return;
  const tag = button.dataset.learningTag;
  if (learningTags.has(tag)) learningTags.delete(tag);
  else learningTags.add(tag);
  document.querySelectorAll('[data-learning-tag]').forEach((node) => node.setAttribute('aria-pressed', String(learningTags.has(node.dataset.learningTag))));
  document.querySelector('#learning-clear-tag').disabled = !learningTags.size;
  renderLearningSearch();
  renderLearningDialog();
});
document.querySelector('#learning-clear-tag')?.addEventListener('click', () => {
  learningTags.clear();
  document.querySelectorAll('[data-learning-tag]').forEach((node) => node.setAttribute('aria-pressed', 'false'));
  document.querySelector('#learning-clear-tag').disabled = true;
  renderLearningSearch();
  renderLearningDialog();
});
document.addEventListener('click', (event) => {
  if (!event.target.closest('.learning-search-wrap') && !event.target.closest('#learning-tags')) {
    learningSearchOpen = false;
    renderLearningSearch();
  }
});

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
  const dialog = document.querySelector('#learning-all-dialog');
  if (dialog?.open) dialog.close();
  learningSearchOpen = false;
  document.querySelector('#learning-search').value = '';
  renderLearningSearch();
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
