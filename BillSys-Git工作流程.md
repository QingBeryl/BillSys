# BillSys Git 工作流程

> 主分支：**master** ｜ 开发分支：**dev/szdjf** ｜ 不直接 push master，只通过 PR 合入。

---

## 一、每天写代码前（同步最新）

```bash
git checkout master
git pull origin master
```
> 📍 远程 master → 本地 master → 工作区文件更新（完全对齐远程）

```bash
git checkout dev/szdjf
git merge master
```
> 📍 本地 master 的 commit → 合入本地 dev/szdjf → 工作区文件更新

```bash
# 有冲突时：
git add 冲突的文件
git commit -m "merge: 同步 master 最新代码"
```

```bash
git push origin dev/szdjf
```
> 📍 本地 dev/szdjf → 远程 dev/szdjf

---

## 二、写完代码，提交并合入 master

```bash
git checkout dev/szdjf
```
> 📍 确认在开发分支上

```bash
git status
```

```bash
git add backend/routes/auth.py frontend/src/views/Register.vue
```
> 📍 工作区 → 暂存区

```bash
git commit -m "feat: 添加用户注册功能"
```
> 📍 暂存区 → 本地仓库（dev/szdjf 分支）

```bash
git push origin dev/szdjf
```
> 📍 本地仓库 → 远程 dev/szdjf（GitHub 可见）

```bash
# GitHub 网页：Compare & pull request → 合作者 Merge
```
> 📍 远程 dev/szdjf → 远程 master

---

## 三、代码流向总图

```
工作区（你改的文件）
  ↓ git add
暂存区
  ↓ git commit
本地 dev/szdjf
  ↓ git push
远程 dev/szdjf
  ↓ PR → Merge
远程 master
  ↓ git pull
本地 master
  ↓ git merge master（在 dev/szdjf 上）
本地 dev/szdjf（起点更新，继续开发）
```

---

## 四、其他常用

```bash
# 本地没有 master 时（第一次）
git fetch origin
git checkout master

# 查看
git branch -a
git log --oneline -10

# 撤销
git checkout -- 文件名          # 没 add，恢复文件
git reset HEAD 文件名           # 已 add 没 commit，取消暂存
git reset --soft HEAD~1        # 已 commit 没 push，回退一个 commit

# 分支
git checkout -b dev/新分支名
git branch -d 分支名
git push origin --delete 分支名

# 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## 五、commit message 规范

`feat:` 新功能 ｜ `fix:` 修 bug ｜ `refactor:` 重构 ｜ `chore:` 杂务 ｜ `docs:` 文档
