+++
date = '2025-12-12T14:05:41-08:00'
title = 'Website Setup'
+++

Today I wanted to create a personal website. I wanted a minimal setup that didn't require me to fiddle with any frontend code, which I already do more than enough at my day job. With this setup, creating new posts is as simple as creating markdown files and pushing them to GitHub.

After half an hour of research, I landed on the current setup, which uses [Hugo](https://gohugo.io/), [GitHub](https://github.com/), and [Cloudflare Pages](https://pages.cloudflare.com/)[^1]. 

[^1]: I chose Cloudflare Pages as I already use it to deploy my [crossword leaderboard](https://crosselo.avigupta.workers.dev/), and I like that it provides clean domain names (`*.pages.dev`) for free.

I was able to get this setup working in about 20 minutes on macOS. Note that these instructions are largely adapted from Cloudflare's [tutorial](https://developers.cloudflare.com/pages/framework-guides/deploy-a-hugo-site/) on deploying a Hugo site, with some modifications (using a different theme, adding a `.gitignore`, etc).

1. Install hugo and create a new project
    ```
    brew install hugo
    hugo new site avig
    ```

2. Initialize a local Git repository

    ```
    cd avig
    git init
    git submodule add https://github.com/yihui/hugo-xmin.git themes/xmin
    echo "theme = 'xmin'" >> hugo.toml
    echo "/public/" >> .gitignore
    ```
    Replace the theme here with whatever theme you like.


3. Create your first post
    ```
    hugo new content posts/hello-world.md
    ```

    Remove `draft: true` from the resulting file so that hugo will publish it during the build step.

4. Create a GitHub repository and push your local repo

    [Create a new repository on GitHub](https://github.com/new) and then push to it:
    ```
    git remote add origin git@github.com:aviguptatx/avig.git
    git add .
    git commit -m "first commit"
    git push -u origin main
    ```

5. Deploy the GitHub repository via Cloudflare Pages

    Follow [this tutorial](https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/) to integrate a Cloudflare Pages deployment with the GitHub repository you created in the previous step. When configuring the deployment, you should have the option to select `Hugo` as your build preset. If not, manually set the build command to `hugo` and the build output directory to `/public`.

That's it! Making changes is as simple as creating new markdown files and pushing to GitHub -- Cloudfare Pages will automatically update the site within ~20s of pushing to GitHub.
