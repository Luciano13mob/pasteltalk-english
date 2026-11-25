from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "0.0.0.0"
PORT = 8000

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PastelTalk — English Roleplay App</title>
  <style>
    :root {
      --bg-cream: #fdfbf7;
      --card-white: #ffffff;
      --lavender-soft: #ede9fe;
      --lavender-accent: #8b5cf6;
      --mint-soft: #dcfce7;
      --mint-accent: #16a34a;
      --peach-soft: #ffedd5;
      --peach-accent: #ea580c;
      --sky-soft: #e0f2fe;
      --sky-accent: #0284c7;
      --rose-soft: #ffe4e6;
      --rose-accent: #e11d48;
      --text-main: #1e293b;
      --text-muted: #64748b;
      --border-soft: #e2e8f0;
      --shadow-soft: 0 10px 30px rgba(148, 163, 184, 0.16);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
      background: linear-gradient(135deg, #fdfbf7 0%, #f3e8ff 50%, #e0f2fe 100%);
      min-height: 100vh;
      color: var(--text-main);
      padding: 28px 16px;
    }

    .container {
      max-width: 860px;
      margin: 0 auto;
    }

    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 22px;
    }

    .brand h1 {
      font-size: 1.65rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .brand p {
      color: var(--text-muted);
      font-size: 0.92rem;
      margin-top: 2px;
    }

    .score-badge {
      background: var(--card-white);
      border: 1px solid var(--border-soft);
      box-shadow: var(--shadow-soft);
      padding: 10px 18px;
      border-radius: 999px;
      font-weight: 600;
      font-size: 0.95rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .score-pill {
      background: var(--lavender-soft);
      color: var(--lavender-accent);
      padding: 3px 10px;
      border-radius: 999px;
      font-weight: 700;
    }

    .panel {
      background: var(--card-white);
      border: 1px solid rgba(226, 232, 240, 0.9);
      border-radius: 24px;
      box-shadow: var(--shadow-soft);
      padding: 24px;
      margin-bottom: 20px;
    }

    .section-title {
      font-size: 1rem;
      font-weight: 700;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }

    .field label {
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 6px;
    }

    .field input,
    .field select {
      width: 100%;
      padding: 10px 14px;
      border-radius: 14px;
      border: 1px solid var(--border-soft);
      background: var(--bg-cream);
      color: var(--text-main);
      font-size: 0.92rem;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .field input:focus,
    .field select:focus {
      border-color: var(--lavender-accent);
      box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
      background: #fff;
    }

    .scenario-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 18px;
    }

    .tab-btn {
      border: 1px solid var(--border-soft);
      background: var(--bg-cream);
      color: var(--text-main);
      padding: 10px 16px;
      border-radius: 16px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .tab-btn:hover {
      background: var(--sky-soft);
      border-color: #bae6fd;
    }

    .tab-btn.active {
      background: var(--lavender-soft);
      color: var(--lavender-accent);
      border-color: #c4b5fd;
    }

    .npc-banner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      background: var(--sky-soft);
      border-radius: 18px;
      padding: 14px 18px;
      margin-bottom: 18px;
    }

    .npc-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .avatar {
      width: 46px;
      height: 46px;
      border-radius: 15px;
      background: var(--card-white);
      display: grid;
      place-items: center;
      font-size: 1.45rem;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.12);
    }

    .npc-name {
      font-weight: 700;
      font-size: 1rem;
    }

    .npc-meta {
      font-size: 0.82rem;
      color: var(--text-muted);
    }

    .progress-tag {
      font-size: 0.82rem;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.85);
      color: var(--sky-accent);
      padding: 6px 12px;
      border-radius: 999px;
    }

    .chat-box {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 20px;
    }

    .bubble {
      max-width: 82%;
      padding: 14px 16px;
      border-radius: 18px;
      line-height: 1.5;
      font-size: 0.95rem;
    }

    .bubble.npc {
      align-self: flex-start;
      background: var(--lavender-soft);
      border-bottom-left-radius: 6px;
    }

    .bubble.user {
      align-self: flex-end;
      background: var(--mint-soft);
      border-bottom-right-radius: 6px;
    }

    .bubble-label {
      font-size: 0.74rem;
      font-weight: 700;
      opacity: 0.7;
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .choices {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .choice-btn {
      text-align: left;
      width: 100%;
      padding: 14px 16px;
      border-radius: 16px;
      border: 1px solid var(--border-soft);
      background: var(--bg-cream);
      color: var(--text-main);
      font-size: 0.93rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .choice-btn:hover:not(:disabled) {
      background: var(--peach-soft);
      border-color: #fed7aa;
      transform: translateY(-1px);
    }

    .choice-btn:disabled {
      opacity: 0.65;
      cursor: not-allowed;
    }

    .feedback-card {
      margin-top: 16px;
      padding: 16px 18px;
      border-radius: 18px;
      display: none;
    }

    .feedback-card.good {
      display: block;
      background: var(--mint-soft);
      border: 1px solid #86efac;
    }

    .feedback-card.mid {
      display: block;
      background: var(--peach-soft);
      border: 1px solid #fdba74;
    }

    .feedback-card.low {
      display: block;
      background: var(--rose-soft);
      border: 1px solid #fda4af;
    }

    .feedback-title {
      font-weight: 700;
      font-size: 0.92rem;
      margin-bottom: 4px;
    }

    .feedback-text {
      font-size: 0.89rem;
      line-height: 1.45;
    }

    .actions-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 18px;
    }

    .btn-primary {
      background: var(--lavender-accent);
      color: #ffffff;
      border: none;
      padding: 11px 20px;
      border-radius: 14px;
      font-weight: 600;
      font-size: 0.92rem;
      cursor: pointer;
      transition: opacity 0.2s;
    }

    .btn-primary:hover {
      opacity: 0.92;
    }

    .btn-replay {
      background: var(--peach-soft);
      color: var(--peach-accent);
      border: 1px solid #fed7aa;
      padding: 11px 20px;
      border-radius: 14px;
      font-weight: 600;
      font-size: 0.92rem;
      cursor: pointer;
      transition: background 0.2s;
    }

    .btn-replay:hover {
      background: #ffedd5;
    }

    .summary-box {
      display: none;
      text-align: center;
      padding: 20px;
      border-radius: 20px;
      background: var(--lavender-soft);
      margin-top: 14px;
    }

    .summary-box.show {
      display: block;
    }

    .summary-box h3 {
      font-size: 1.25rem;
      margin-bottom: 8px;
    }

    .summary-box p {
      color: var(--text-muted);
      margin-bottom: 16px;
      font-size: 0.94rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <h1>PastelTalk English</h1>
        <p>Latihan percakapan bahasa Inggris interaktif berbasis roleplay</p>
      </div>
      <div class="score-badge">
        <span>Skor Kamu</span>
        <span class="score-pill" id="scoreValue">0 pts</span>
      </div>
    </header>

    <!-- Kustomisasi NPC -->
    <section class="panel">
      <div class="section-title">Kustomisasi Lawan Bicara (NPC)</div>
      <div class="grid-2">
        <div class="field">
          <label for="npcNameInput">Nama NPC</label>
          <input id="npcNameInput" type="text" value="Maya" maxlength="24" />
        </div>
        <div class="field">
          <label for="npcRoleInput">Peran / Profesi NPC</label>
          <input id="npcRoleInput" type="text" value="Barista Cafe" maxlength="32" />
        </div>
        <div class="field">
          <label for="npcToneSelect">Gaya Bicara NPC</label>
          <select id="npcToneSelect">
            <option value="Friendly & Warm">Friendly &amp; Warm</option>
            <option value="Polite & Formal">Polite &amp; Formal</option>
            <option value="Energetic & Casual">Energetic &amp; Casual</option>
          </select>
        </div>
        <div class="field">
          <label for="npcAvatarSelect">Avatar NPC</label>
          <select id="npcAvatarSelect">
            <option value="☕">☕ Cangkir Kopi</option>
            <option value="💼">💼 Profesional</option>
            <option value="✈️">✈️ Traveler</option>
            <option value="🌸">🌸 Bunga Pastel</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Area Roleplay -->
    <section class="panel">
      <div class="scenario-tabs" id="scenarioTabs"></div>

      <div class="npc-banner">
        <div class="npc-info">
          <div class="avatar" id="npcAvatarDisplay">☕</div>
          <div>
            <div class="npc-name" id="npcTitleDisplay">Maya — Barista Cafe</div>
            <div class="npc-meta" id="npcToneDisplay">Gaya bicara: Friendly &amp; Warm</div>
          </div>
        </div>
        <div class="progress-tag" id="progressTag">Giliran 1 / 2</div>
      </div>

      <div class="chat-box" id="chatBox"></div>
      <div class="choices" id="choicesBox"></div>

      <div class="feedback-card" id="feedbackCard">
        <div class="feedback-title" id="feedbackTitle"></div>
        <div class="feedback-text" id="feedbackText"></div>
      </div>

      <div class="summary-box" id="summaryBox">
        <h3 id="summaryHeading">Skenario Selesai!</h3>
        <p id="summaryDesc"></p>
        <button class="btn-replay" id="summaryReplayBtn">Main Lagi</button>
      </div>

      <div class="actions-row">
        <button class="btn-replay" id="replayBtn">Main Lagi</button>
        <button class="btn-primary" id="nextTurnBtn" style="display: none;">Lanjut Giliran →</button>
      </div>
    </section>
  </div>

  <script>
    const SCENARIOS = [
      {
        id: "cafe",
        title: "☕ Memesan di Cafe",
        defaultNpc: { name: "Maya", role: "Barista Cafe", tone: "Friendly & Warm", avatar: "☕" },
        turns: [
          {
            npcLine: "Hi there! Welcome to Pastel Brew. What can I get started for you today?",
            options: [
              {
                text: "Could I have an iced latte with oat milk, please?",
                points: 20,
                level: "good",
                feedback: "Sangat natural dan sopan! Frasa 'Could I have...' sangat umum dipakai saat memesan makanan atau minuman."
              },
              {
                text: "Give me coffee now.",
                points: 5,
                level: "low",
                feedback: "Terlalu langsung dan terdengar kurang sopan. Tambahkan 'Could I have...' atau 'I'd like...' agar lebih ramah."
              },
              {
                text: "I want iced latte.",
                points: 12,
                level: "mid",
                feedback: "Cukup jelas dan bisa dipahami, namun menambahkan 'please' atau 'I'd like...' akan terdengar lebih halus."
              }
            ]
          },
          {
            npcLine: "Sure thing! Would you like that to stay or to go?",
            options: [
              {
                text: "For here, please. I'm going to read for a bit.",
                points: 20,
                level: "good",
                feedback: "Bagus sekali! 'For here' adalah jawaban tepat untuk 'to stay' (minum/makan di tempat)."
              },
              {
                text: "Yes, I am fine.",
                points: 5,
                level: "low",
                feedback: "Kurang menjawab pertanyaan pilihan tempat. Gunakan 'For here' (di sini) atau 'To go' (dibawa pulang)."
              },
              {
                text: "To go, thank you.",
                points: 18,
                level: "good",
                feedback: "Tepat dan jelas! 'To go' (atau 'Takeaway' di Inggris/Australia) pas untuk pesanan dibawa pulang."
              }
            ]
          }
        ]
      },
      {
        id: "interview",
        title: "💼 Wawancara Singkat",
        defaultNpc: { name: "Daniel", role: "HR Coordinator", tone: "Polite & Formal", avatar: "💼" },
        turns: [
          {
            npcLine: "Good morning! Thanks for coming in. Could you briefly introduce yourself?",
            options: [
              {
                text: "Good morning! I'm a final-year student passionate about clear communication and teamwork.",
                points: 20,
                level: "good",
                feedback: "Hebat! Pembukaan yang percaya diri, ringkas, dan relevan untuk suasana wawancara."
              },
              {
                text: "I don't know, just me.",
                points: 5,
                level: "low",
                feedback: "Terlalu singkat untuk wawancara. Sebutkan latar belakang singkat dan minat utamamu."
              },
              {
                text: "My name is... uh, I study English.",
                points: 12,
                level: "mid",
                feedback: "Sudah memuat informasi dasar, tapi bisa diperkuat dengan kalimat penuh yang lebih terstruktur."
              }
            ]
          },
          {
            npcLine: "Why are you interested in joining our team this semester?",
            options: [
              {
                text: "I'd love to contribute my organizational skills while learning from your team.",
                points: 20,
                level: "good",
                feedback: "Sangat baik! Menunjukkan kontribusi sekaligus kemauan belajar adalah kombinasi ideal."
              },
              {
                text: "Because my friend told me to apply.",
                points: 5,
                level: "low",
                feedback: "Kurang menunjukkan motivasi pribadi. Fokuslah pada nilai atau pengalaman yang ingin kamu kembangkan."
              },
              {
                text: "I think this place looks nice and friendly.",
                points: 13,
                level: "mid",
                feedback: "Cukup positif, namun akan lebih kuat jika dikaitkan dengan peran atau keterampilanmu."
              }
            ]
          }
        ]
      },
      {
        id: "airport",
        title: "✈️ Tanya Arah di Bandara",
        defaultNpc: { name: "Leo", role: "Airport Info Desk", tone: "Energetic & Casual", avatar: "✈️" },
        turns: [
          {
            npcLine: "Hey there! Need help finding your gate or check-in counter?",
            options: [
              {
                text: "Excuse me, could you tell me where Gate B4 is?",
                points: 20,
                level: "good",
                feedback: "Sangat sopan dan jelas! 'Excuse me, could you tell me where...' adalah pola klasik yang sangat berguna."
              },
              {
                text: "Gate B4 where?",
                points: 8,
                level: "low",
                feedback: "Bisa dimengerti saat terburu-buru, tetapi susunan kalimatnya belum baku. Coba 'Where is Gate B4?'."
              },
              {
                text: "Where is Gate B4, please?",
                points: 16,
                level: "mid",
                feedback: "Langsung pada inti dan sopan. Menambahkan 'Excuse me' di awal akan membuatnya makin halus."
              }
            ]
          },
          {
            npcLine: "It's straight ahead past security, about a five-minute walk. Anything else?",
            options: [
              {
                text: "That's super helpful. Thanks so much for your help!",
                points: 20,
                level: "good",
                feedback: "Natural dan hangat! Ungkapan apresiasi seperti ini menutup percakapan dengan sangat baik."
              },
              {
                text: "Okay.",
                points: 6,
                level: "low",
                feedback: "Terlalu datar. Tambahkan ucapan terima kasih seperti 'Thanks!' atau 'Got it, thank you!'."
              },
              {
                text: "Got it, thank you!",
                points: 17,
                level: "good",
                feedback: "Singkat, jelas, dan tetap sopan."
              }
            ]
          }
        ]
      }
    ];

    let currentScenarioIndex = 0;
    let currentTurnIndex = 0;
    let totalScore = 0;
    let answeredCurrentTurn = false;

    const el = {
      scoreValue: document.getElementById("scoreValue"),
      npcNameInput: document.getElementById("npcNameInput"),
      npcRoleInput: document.getElementById("npcRoleInput"),
      npcToneSelect: document.getElementById("npcToneSelect"),
      npcAvatarSelect: document.getElementById("npcAvatarSelect"),
      scenarioTabs: document.getElementById("scenarioTabs"),
      npcAvatarDisplay: document.getElementById("npcAvatarDisplay"),
      npcTitleDisplay: document.getElementById("npcTitleDisplay"),
      npcToneDisplay: document.getElementById("npcToneDisplay"),
      progressTag: document.getElementById("progressTag"),
      chatBox: document.getElementById("chatBox"),
      choicesBox: document.getElementById("choicesBox"),
      feedbackCard: document.getElementById("feedbackCard"),
      feedbackTitle: document.getElementById("feedbackTitle"),
      feedbackText: document.getElementById("feedbackText"),
      nextTurnBtn: document.getElementById("nextTurnBtn"),
      replayBtn: document.getElementById("replayBtn"),
      summaryBox: document.getElementById("summaryBox"),
      summaryHeading: document.getElementById("summaryHeading"),
      summaryDesc: document.getElementById("summaryDesc"),
      summaryReplayBtn: document.getElementById("summaryReplayBtn")
    };

    function getScenario() {
      return SCENARIOS[currentScenarioIndex];
    }

    function syncNpcDefaultsToInputs() {
      const npc = getScenario().defaultNpc;
      el.npcNameInput.value = npc.name;
      el.npcRoleInput.value = npc.role;
      el.npcToneSelect.value = npc.tone;
      el.npcAvatarSelect.value = npc.avatar;
      renderNpcHeader();
    }

    function renderNpcHeader() {
      const name = el.npcNameInput.value.trim() || "NPC";
      const role = el.npcRoleInput.value.trim() || "Partner";
      const tone = el.npcToneSelect.value;
      const avatar = el.npcAvatarSelect.value;

      el.npcAvatarDisplay.textContent = avatar;
      el.npcTitleDisplay.textContent = `${name} — ${role}`;
      el.npcToneDisplay.textContent = `Gaya bicara: ${tone}`;
    }

    function renderScenarioTabs() {
      el.scenarioTabs.innerHTML = "";
      SCENARIOS.forEach((sc, idx) => {
        const btn = document.createElement("button");
        btn.className = "tab-btn" + (idx === currentScenarioIndex ? " active" : "");
        btn.textContent = sc.title;
        btn.addEventListener("click", () => {
          currentScenarioIndex = idx;
          syncNpcDefaultsToInputs();
          resetScenarioState();
          renderScenarioTabs();
        });
        el.scenarioTabs.appendChild(btn);
      });
    }

    function addBubble(senderType, label, text) {
      const div = document.createElement("div");
      div.className = `bubble ${senderType}`;
      div.innerHTML = `<div class="bubble-label">${label}</div><div>${text}</div>`;
      el.chatBox.appendChild(div);
    }

    function renderTurn() {
      const scenario = getScenario();
      const turn = scenario.turns[currentTurnIndex];
      const npcName = el.npcNameInput.value.trim() || "NPC";

      answeredCurrentTurn = false;
      el.feedbackCard.className = "feedback-card";
      el.feedbackCard.style.display = "none";
      el.nextTurnBtn.style.display = "none";
      el.summaryBox.classList.remove("show");

      el.progressTag.textContent = `Giliran ${currentTurnIndex + 1} / ${scenario.turns.length}`;
      addBubble("npc", npcName, turn.npcLine);

      el.choicesBox.innerHTML = "";
      turn.options.forEach((opt) => {
        const btn = document.createElement("button");
        btn.className = "choice-btn";
        btn.textContent = opt.text;
        btn.addEventListener("click", () => handleSelectOption(opt));
        el.choicesBox.appendChild(btn);
      });
    }

    function handleSelectOption(option) {
      if (answeredCurrentTurn) return;
      answeredCurrentTurn = true;

      document.querySelectorAll(".choice-btn").forEach((b) => (b.disabled = true));

      addBubble("user", "Kamu", option.text);

      totalScore += option.points;
      el.scoreValue.textContent = `${totalScore} pts`;

      el.feedbackCard.className = `feedback-card ${option.level}`;
      el.feedbackCard.style.display = "block";
      el.feedbackTitle.textContent = `Feedback (+${option.points} pts)`;
      el.feedbackText.textContent = option.feedback;

      const scenario = getScenario();
      if (currentTurnIndex < scenario.turns.length - 1) {
        el.nextTurnBtn.style.display = "inline-block";
      } else {
        el.choicesBox.innerHTML = "";
        el.summaryHeading.textContent = `Skenario "${scenario.title}" Selesai!`;
        el.summaryDesc.textContent = `Total skor kamu saat ini: ${totalScore} pts. Kamu bisa lanjut ke skenario lain atau klik Main Lagi untuk mengulang.`;
        el.summaryBox.classList.add("show");
      }
    }

    function resetScenarioState() {
      currentTurnIndex = 0;
      el.chatBox.innerHTML = "";
      el.choicesBox.innerHTML = "";
      renderTurn();
    }

    function replayAll() {
      totalScore = 0;
      el.scoreValue.textContent = "0 pts";
      resetScenarioState();
    }

    [el.npcNameInput, el.npcRoleInput, el.npcToneSelect, el.npcAvatarSelect].forEach((input) => {
      input.addEventListener("input", renderNpcHeader);
      input.addEventListener("change", renderNpcHeader);
    });

    el.nextTurnBtn.addEventListener("click", () => {
      currentTurnIndex += 1;
      renderTurn();
    });

    el.replayBtn.addEventListener("click", replayAll);
    el.summaryReplayBtn.addEventListener("click", replayAll);

    // Inisialisasi awal
    renderScenarioTabs();
    syncNpcDefaultsToInputs();
    resetScenarioState();
  </script>
</body>
</html>
"""


class RoleplayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = HTML_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/health":
            payload = json.dumps({"status": "ok"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Menjaga log terminal tetap bersih
        return


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), RoleplayHandler)
    print(f"Server berjalan di http://{HOST}:{PORT} (Tekan Ctrl+C untuk berhenti)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
        server.server_close()