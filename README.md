# Fedilink - Simplifying fediverse interactions

This is an azure functions app that allows for smoother links to fediverse links

## The problem

When you share a link to a Mastodon toot, such as https://mas.to/@moof/109642947257051795 this takes you to the toot in question, regardless of what your home Mastodon server is, you will get sent to [mas.to](https://mas.to/)

If your main account is on a different fediverse server, say [masto.nu](https://masto.nu), it creates a problem when you want to boost, favourite, or reply to the toot. You have to manually head to masto.nu, and paste the link to mas.to into the search bar, before clicking on links to perform the boosting, favouriting, or replying. It's an extra step that is annoying, and makes interaction more difficult, and thus less likely to happen for casual stuff.

## The proposed solution

When you paste a URL that you are sharing, add https://fedi.link/ (or https://masto.link/) to the front of the URL. So the above URL becomes https://fedi.link/https://mas.to/@moof/109642947257051795.

When you first go to a fedi.link link you get a splash page inviting you to put your own mastodon instance name into the system, so that if you put https://masto.nu into that space, you will get redirected to https://masto.nu/@moof@mas.to/109642947257051795, which is the same toot, but from your own instance, so you can interact with it directly if you so wish.

## How it works

The first few times that you go to a fedi.link URL you get the option of setting your instance link, or going direct to the mastodon post. It stores your instance account in a cookie, with no additional personal information. When you next go to a fedi.link url, it will take you straight to your instance, without asking any further.
