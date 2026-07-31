add# BillSys Git 工作流程

> 主分支：**master** ｜ 开发分支：**dev/szdjf** ｜ 不直接 push master，只通过 PR 合入。

---

## 一、每天写代码前（同步最新）

```bash
git checkout master
```
> 📍 你的文件夹内容 → 变成 master 的版本
> 你之前改的代码不会丢（存在 dev/szdjf 里），只是当前看到的文件换了

```bash
git pull origin master
```
> 📍 远程 GitHub 上的 master → 下载到你本地 master → 文件夹内容更新
> 远程多了什么文件 → 你本地也会出现
> 远程删了什么文件 → 你本地也会消失
> 远程改了什么文件 → 你本地也变成最新的

```bash
git checkout dev/szdjf
```
> 📍 你的文件夹内容 → 变回你自己分支的版本

```bash
git merge master
```
> 📍 master 里的新代码 → 合进你当前的 dev/szdjf → 文件夹内容更新
> 合完之后你看到的文件 = master 最新的 + 你自己改的，两边都在
> 如果同一个文件你改了、master 也改了同一处 → 报 CONFLICT，让你手动选保留哪个
> 如果没冲突 → 自动合好，不会覆盖你的东西

```bash
# 有冲突时：手动改完冲突文件后
git add 冲突的文件
git commit -m "merge: 同步 master 最新代码"
```
> 📍 你手动解决后的文件 → 暂存区 → 打包成一个新 commit 存在本地 dev/szdjf

```bash
git push origin dev/szdjf
```
> 📍 本地 dev/szdjf → 上传到 GitHub 的 dev/szdjf
> 不推也行，只是 GitHub 上看不到你刚合并的结果

---

## 二、写完代码，提交并合入 master

```bash
git checkout dev/szdjf
```
> 📍 确认你在自己的开发分支上，文件夹里看到的是你的代码

```bash
git status
```
> 📍 不改任何东西，只是告诉你：哪些文件被你改过了、哪些还没暂存

```bash
git add backend/routes/auth.py frontend/src/views/Register.vue
```
> 📍 你改的文件（工作区）→ 放进"待打包清单"（暂存区）
> 没 add 的文件就算改了也不会被提交

```bash
git commit -m "feat: 添加用户注册功能"
```
> 📍 暂存区里的文件 → 打包成一个存档点（commit），存在本地 .git 里
> 此时只有你自己电脑能看到，GitHub 上还没有

```bash
git push origin dev/szdjf
```
> 📍 本地的 commit → 上传到 GitHub 的 dev/szdjf 分支
> 现在合作者能在 GitHub 上看到你的代码了，但还没进 master

```bash
# GitHub 网页：Compare & pull request → 合作者 review → 点 Merge
```
> 📍 GitHub 上的 dev/szdjf → 合入 GitHub 上的 master
> 此时你本地还不知道这件事，下次写代码前做一遍第一节就同步了

---

## 三、代码流向总图

```
你改了文件（工作区）
  ↓ git add
待打包清单（暂存区）
  ↓ git commit
本地 dev/szdjf（.git 文件夹里的一个存档）
  ↓ git push
GitHub 上的 dev/szdjf（别人能看到了）
  ↓ 开 PR → 合作者点 Merge
GitHub 上的 master（正式代码）
  ↓ git pull（在本地 master 上）
本地 master（和 GitHub 对齐）
  ↓ git merge master（在 dev/szdjf 上）
本地 dev/szdjf（你的起点更新了，继续写代码）
```

---

## 四、其他常用

```bash
# 本地没有 master 时（第一次）
git fetch origin          # 把 GitHub 上的分支信息下载到本地
git checkout master       # 自动创建本地 master，内容和 GitHub 的 master 一样
```

```bash
# 查看
git branch -a             # 列出所有分支（本地 + 远程）
git log --oneline -10     # 最近 10 条 commit 记录
```

```bash
# 撤销
git checkout -- 文件名    # 你改了文件但没 add → 恢复成上次 commit 的样子，改动消失
git reset HEAD 文件名     # 你已经 add 了但没 commit → 从暂存区退回工作区，文件内容不变
git reset --soft HEAD~1  # 你已经 commit 了但没 push → 撤销这个 commit，改动退回工作区
```

```bash
# 分支
git checkout -b dev/新分支名    # 创建一个新分支并切过去
git branch -d 分支名            # 删除本地分支（已合并的才能删）
git push origin --delete 分支名 # 删除 GitHub 上的远程分支
```

```bash
# 代理（连不上 GitHub 时）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## 五、commit message 规范

`feat:` 新功能 ｜ `fix:` 修 bug ｜ `refactor:` 重构 ｜ `chore:` 杂务 ｜ `docs:` 文档
