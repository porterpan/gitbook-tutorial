# git 相关命令学习

##1. [git remote 命令用法](https://www.git-scm.com/docs/git-remote)

```bash
git remote [-v | --verbose]  #不带参数，列出已经存在的远程分支
git remote add [-t <branch>] [-m <master>] [-f] [--[no-]tags] [--mirror=<fetch|push>] <name> <url>
git remote rename <old> <new>
git remote remove <name>
git remote set-head <name> (-a | --auto | -d | --delete | <branch>)
git remote set-branches [--add] <name> <branch>…​
git remote get-url [--push] [--all] <name>
git remote set-url [--push] <name> <newurl> [<oldurl>]
git remote set-url --add [--push] <name> <newurl>
git remote set-url --delete [--push] <name> <url>
git remote [-v | --verbose] show [-n] <name>…​
git remote prune [-n | --dry-run] <name>…​
git remote [-v | --verbose] update [-p | --prune] [(<group> | <remote>)…​]
```

##例程代码

* 查看当前的远程库 

```shell
$ git remote -v
  origin git://github.com/schacon/ticgit.git如果有多个远程仓库,此命令将全部列出.比如在我的 Grit 项目中,可以看到.

$ git remote #不带参数，列出已经存在的远程分支
  origin
```


