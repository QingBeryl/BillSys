# BillSys Git 工作流程

## 一、我改完代码，提交并合入 main

```bash
# 1. 确认在自己的开发分支上
git checkout dev/你的分支名

# 2. 查看改了哪些文件
git status

# 3. 暂存（只加你改的，别 git add .）
git add backend/routes/auth.py frontend/src/views/Register.vue

# 4. 提交（一个功能一个 commit，message 写清楚）
git commit -m "feat: 添加用户注册功能"

# 5. 推送到远程自己的分支
git push origin dev/你的分支名

# 6. 打开 GitHub → 仓库页面 → 点 "Compare & pull request"
#    填标题和描述 → Create pull request
#    等合作者 review + approve → 他在网页上点 Merge
```

commit message 规范：
- `feat: xxx` — 新功能
- `fix: xxx` — 修 bug
- `refactor: xxx` — 重构（功能不变，改结构）
- `chore: xxx` — 杂务（改配置、加 .gitignore 等）
- `docs: xxx` — 改文档

## 二、拉取别人合入 main 的代码

```bash
# 1. 切到 main，拉最新
git checkout main
git pull origin main

# 2. 切回自己分支，把 main 的新内容合进来
git checkout dev/你的分支名
git merge main

# 3. 如果有冲突（CONFLICT），手动解决后：
git add 冲突的文件
git commit -m "merge: 同步 main 最新代码"

# 4. 推送（让自己远程分支也保持同步）
git push origin dev/你的分支名
```

建议：每天开始写代码前先做一遍，保证起点是最新的。

## 三、其他常用操作

### 查看状态
```bash
git branch -a          # 所有分支（本地+远程）
git status             # 当前改了哪些文件
git log --oneline -10  # 最近10条提交记录
```

### 撤销操作
```bash
# 改坏了，还没 add → 恢复单个文件
git checkout -- backend/app.py

# 已经 add 了但没 commit → 取消暂存
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

## 四、核心原则

1. **永远不直接 push main**，只通过 PR 合入
2. **一个 PR 只做一件事**，别攒一堆功能一起提
3. **自己的分支不删**，一直用，做完一个功能发一次 PR
4. **push 之前先 pull main 合进来**，减少冲突
5. **commit 要勤**，小步提交，别攒一天一次大 commit
