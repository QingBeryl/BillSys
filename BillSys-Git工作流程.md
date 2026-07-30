# BillSys Git 工作流程

> 我们的仓库：主分支是 **master**，个人开发分支是 **dev/szdjf**。
> 永远不直接 push master，只通过 PR 合入。

---

## 零、先搞懂：代码住在哪

Git 里你的代码会经过 **四个位置**，从左到右依次是：

```
工作区          暂存区           本地仓库          远程仓库(GitHub)
(你改的文件)    (git add 后)     (git commit 后)   (git push 后)
```

| 操作 | 代码从哪到哪 |
|------|-------------|
| 你改了文件 | 代码在**工作区**（就是你硬盘上的文件） |
| `git add` | 代码从工作区 → **暂存区**（"待打包清单"） |
| `git commit` | 代码从暂存区 → **本地仓库**（.git 文件夹里的一个存档点） |
| `git push` | 代码从本地仓库 → **远程仓库**（GitHub 服务器上） |
| `git pull` | 代码从远程仓库 → **本地仓库** → 自动合并到工作区 |
| `git merge X` | X 分支的 commit 合入你**当前分支**的本地仓库 |

记住：**没 push 的东西只有你自己电脑上能看到**，别人看不到。

---

## 一、我改完代码，提交并合入 master

```bash
# 1. 确认在自己的开发分支上
git checkout dev/szdjf
```
> 📍 此时你在 dev/szdjf 分支，改的文件都在**工作区**。

```bash
# 2. 查看改了哪些文件
git status
```

```bash
# 3. 暂存（只加你改的，别 git add .）
git add backend/routes/auth.py frontend/src/views/Register.vue
```
> 📍 这两个文件从工作区 → **暂存区**。其他文件就算改了也不会被打包。

```bash
# 4. 提交
git commit -m "feat: 添加用户注册功能"
```
> 📍 暂存区的内容打包成一个 commit，存入**本地仓库**（dev/szdjf 分支上）。
> 此时 GitHub 上还看不到这个改动。

```bash
# 5. 推送到远程自己的分支
git push origin dev/szdjf
```
> 📍 commit 从本地仓库 → **GitHub 远程仓库**的 dev/szdjf 分支。
> 现在合作者能在 GitHub 上看到你的代码了，但还没进 master。

```bash
# 6. 打开 GitHub → 仓库页面 → 点 "Compare & pull request"
#    填标题和描述 → Create pull request
#    等合作者 review + approve → 他在网页上点 Merge
```
> 📍 Merge 之后：你 dev/szdjf 上的 commit 被合入**远程 master**。
> 但注意！你本地的 master 还不知道这件事，需要 pull 才能同步（见第二节）。

### commit message 规范

- `feat: xxx` — 新功能
- `fix: xxx` — 修 bug
- `refactor: xxx` — 重构（功能不变，改结构）
- `chore: xxx` — 杂务（改配置、加 .gitignore 等）
- `docs: xxx` — 改文档

---

## 二、拉取别人合入 master 的代码

```bash
# 1. 切到 master，拉最新
git checkout master
git pull origin master
```
> 📍 远程 master 的新 commit → 你**本地的 master 分支** → 工作区文件更新。

```bash
# 2. 切回自己分支，把 master 的新内容合进来
git checkout dev/szdjf
git merge master
```
> 📍 master 上的 commit 合入你**当前所在的 dev/szdjf 分支**。
> 合完之后，你的 dev/szdjf 就包含了 master 的所有最新代码 + 你自己的改动。
> 代码还在本地，GitHub 上的 dev/szdjf 还没更新。

```bash
# 3. 如果有冲突（CONFLICT），手动解决后：
git add 冲突的文件
git commit -m "merge: 同步 master 最新代码"
```
> 📍 解决冲突本身也会产生一个新 commit，存在本地 dev/szdjf 上。

```bash
# 4. 推送（让自己远程分支也保持同步）
git push origin dev/szdjf
```
> 📍 合并后的 dev/szdjf → GitHub。现在远程 dev/szdjf 也包含 master 的最新内容了。

**建议：每天开始写代码前先做一遍，保证起点是最新的。**

---

## 三、代码流向总图

一次完整的"改代码 → 上线"流程，代码的旅程：

```
你改了文件
    ↓ git add
暂存区（待打包）
    ↓ git commit
本地 dev/szdjf（只有你能看到）
    ↓ git push
远程 dev/szdjf（GitHub 上能看到）
    ↓ 开 PR → 合作者 Merge
远程 master（正式代码）
    ↓ 你 git pull + merge
本地 master → 本地 dev/szdjf（你的起点更新了）
```

---

## 四、其他常用操作

### 查看状态
```bash
git branch -a          # 所有分支（本地+远程）
git status             # 当前改了哪些文件
git log --oneline -10  # 最近10条提交记录
```

### 撤销操作
```bash
# 改坏了，还没 add → 恢复单个文件（代码从工作区消失，回到上次 commit 的状态）
git checkout -- backend/app.py

# 已经 add 了但没 commit → 取消暂存（代码退回工作区，文件内容不变）
git reset HEAD backend/app.py

# 已经 commit 了但没 push → 回退到上一个 commit（改动保留在工作区）
git reset --soft HEAD~1
```

### 分支操作
```bash
git checkout -b dev/新分支名   # 创建并切换到新分支
git branch -d 分支名           # 删除本地已合并的分支
git push origin --delete 分支名 # 删除远程分支
git branch -m 旧名 新名        # 重命名当前分支
```

### 代理（连不上 GitHub 时）
```bash
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## 五、核心原则

1. **永远不直接 push master**，只通过 PR 合入
2. **一个 PR 只做一件事**，别攒一堆功能一起提
3. **自己的分支不删**，一直用，做完一个功能发一次 PR
4. **push 之前先 pull master 合进来**，减少冲突
5. **commit 要勤**，小步提交，别攒一天一次大 commit
