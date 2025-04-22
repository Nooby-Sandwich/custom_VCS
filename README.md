---

### 📦 custom_VCS – *Wen: Your Lightweight Version Control System*

**Wen** is a minimal, Git-inspired version control system built entirely in Python. It’s designed for simplicity, clarity, and experimentation.

---

#### 🚀 Features

- `wen seed` – Initialize a new Wen repository.
- `wen pulse "message"` – Commit changes with a message.
- `wen ripple` – View the commit log.
- `wen tag <name> <message>` – Tag commits.
- `wen sprout <name>` – Create a new branch.
- `wen graft <branch>` – Merge another branch into the current.
- `wen echo` – Show the state of the latest pulse.
- `wen link <subcommand>` – Manage remotes (add/remove/list).
- `wen transmit <remote>` – Push to a remote GitHub repository.
- `wen carry <remote>` – Pull from a remote GitHub repository.

---

#### 🛠 Setup Instructions

```bash
git clone https://github.com/Nooby-Sandwich/custom_VCS.git
cd custom_VCS
python -m venv venv
venv\Scripts\activate    # On Windows
pip install -r requirements.txt
```

Add it to your PATH (optional, for `wen` command):

```bash
setx PATH "%PATH%;C:\path\to\custom_VCS"
```

---

#### 📄 Example Usage

```bash
wen seed
wen pulse "Initial commit"
wen ripple
wen tag v1.0 "First stable snapshot"
wen sprout dev
wen graft dev
```

---

#### 🌐 Remotes

```bash
wen link add origin https://github.com/yourusername/yourrepo.git
wen transmit origin
wen carry origin
```

---

#### 📁 .env Format

```env
DEFAULT_REMOTE=origin
```

---

#### 🧠 Why “Wen”?

Because “when” you wrote that pulse matters — it’s a timeline of your project's life.

---
