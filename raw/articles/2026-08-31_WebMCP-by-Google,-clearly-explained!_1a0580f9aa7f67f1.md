---
title: "WebMCP by Google, clearly explained!"
source_key: "dailydoseofds"
email_subject: "WebMCP By Google, Clearly Explained!"
email_sender: "Daily Dose of DS <avi@dailydoseofds.com>"
email_date: "Mon, 31 Aug 2026 13:43:32 +0000"
email_id: "1a0580f9aa7f67f1"
article_id: "1a0580f9aa7f67f1:2"
published: "2026-08-31"
tags: []
---

# WebMCP by Google, clearly explained!

- **邮件来源**: dailydoseofds
- **原邮件主题**: WebMCP By Google, Clearly Explained!
- **发送人**: Daily Dose of DS <avi@dailydoseofds.com>
- **日期**: Mon, 31 Aug 2026 13:43:32 +0000
- **邮件 ID**: 1a0580f9aa7f67f1
- **文章 ID**: 1a0580f9aa7f67f1:2

---

## **WebMCP by Google, clearly explained!**

When an agent buys something on a website, they usually navigate it via screenshots.

It captures the page, finds something that looks like a button, clicks, waits, and captures again. It reads the screen the way a person would, only slower, and spends tokens in each turn.

![](https://substackcdn.com/image/fetch/$s_!mv2H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c9a7383-bc47-4e43-9f1b-5c0fb5a36a21_1200x896.jpeg)   
---  
  
That works often in a demo, but it is fragile if the website is redesigned.

However, the website already knows exactly what it can do. It has a search, a cart, a checkout, a booking flow, and none of that is written down anywhere a program can read. All of it belongs to a layout that was built for people.

So the failure is not that agents read pages badly. Pages were never written for anything except people.

Here is an example:

[ ](<https://api.filekitcdn.com/e/k7YHPN24SoxyM8nGKZnDxa/pyrWHyJY3TyuEQXyjJLCGb/player>)



WebMCP is a browser API from the Chrome and Edge teams that lets a site write those actions down.

The site names each action, search or add to cart, or book a slot describes it in words a model can read, and lists the inputs it accepts.

WebMCP is one of six ways an agent can reach an app. Going through all six in order shows why this one is the better bet.

#### Six ways an agent can reach an app

The six run from furthest away from the interface to closest to it.

**1) The raw API.** Your script hits the company’s backend directly with an API key. It is precise and fast, but you had to find the endpoints yourself, you manage the key, and the website is never involved.

**2) A backend MCP server.** The company builds a server that describes its actions as named tools, and your agent connects to it. Someone who understands the product defined those tools, which helps, though the user interface is still skipped.

![](https://substackcdn.com/image/fetch/$s_!ILUg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a9db0a1-4ade-4906-9317-7a0506892dee_680x481.webp)   
---  
  
**3) Computer use.** Your agent sees the live page as an image and clicks around. There is nothing to set up. It is slow, every look costs money, and a layout change confuses it.

**4) Browser automation.** Your agent reads the page’s underlying code instead of a picture of it, which is more reliable than pixels. The tools are generic, so the agent still has to work out meaning from anonymous divs and buttons.

![](https://substackcdn.com/image/fetch/$s_!IvqE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd984a0b3-078c-4261-a2ed-881e70084c53_680x462.png)   
---  
  
**5) WebMCP.** The page declares its own actions with names, descriptions, and typed inputs, and your agent calls them.

**6) The site’s built-in assistant.** The company ships its own chat box, picks the model, and pays for the tokens. Your agent stays outside, so you cannot bring your own agent to the site.

![](https://substackcdn.com/image/fetch/$s_!InSb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff7ccba55-3a0c-4a97-9d2c-fa18882bfb91_680x499.png)   
---  
  
#### Problems with the six methods

Three things vary across them. They differ in whose agent does the work, in what the user has to configure before anything happens, and in what the agent receives once it arrives.

![](https://substackcdn.com/image/fetch/$s_!nSe_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6b856e0-29b6-492f-8295-81681b5d8c70_1264x848.jpeg)   
---  
  
Every option except one gives up at least one of the three.

The raw API and the backend MCP server provide clean typed actions, but you do the configuring and the website itself never comes into it.

Computer use needs no setup and hands the agent pixels to work out on its own.

Browser automation gives structure, though it is the same generic structure for every site on the internet.

The built-in assistant is free and precise, and it is not your agent, so nothing it learns about you carries anywhere else.

![](https://substackcdn.com/image/fetch/$s_!BzWg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52af42fa-0e3b-4db1-982c-4e03eb78f777_1200x896.jpeg)   
---  
  
WebMCP keeps all three, since you bring your own agent, you configure nothing, and you get named actions instead of guesswork.

#### Why declaring is better

Instead of the agent working out what a button does, the site says what it does. A few things follow from that.

  * There is no guessing step. The agent gets a list of actions with typed inputs, so there is no interpretation stage where a wrong click quietly does the wrong thing.

![](https://substackcdn.com/image/fetch/$s_!rMR2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F496c0771-fc07-4846-9b14-ee4b95e328fb_1200x896.jpeg)   
---  
  
  * The action runs in the session you are already in. It executes inside your browser tab, so there is no API key for the agent to hold, no separate login, and no token to pass around. You are already signed in, so the agent already has access.
  * The available actions change with the page. A logged-out visitor’s agent sees a handful of read-only actions like search and product lookup. After signing in, the site adds the rest, including order history, cart, and checkout. Nothing special happens on the agent’s side, it just reads the list again.

![](https://substackcdn.com/image/fetch/$s_!Ah3B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc2c0e9f-c7d0-4dd1-a9e6-2ed5a481d357_1264x848.jpeg)   
---  
  
  * Your interface stays in front of the user. The action runs on the visible page, so the user watches it happen, and your product does not get reduced to an API that somebody else’s chat window is calling.
  * Any model can invoke it. Inputs are described with JSON Schema, the same format Claude, GPT, and Gemini already use for tool calling, so you describe your actions once.

#### Setup in code

A tool is a plain JavaScript object handed to the browser. The code goes in your page’s own front-end script, the same JavaScript that already runs when someone loads the site. You register each tool once on page load, and from then on any agent visiting that page can see it and call it.

`document.modelContext.registerTool({  
name: "add_to_cart",  
description: "Add a product to the shopping cart",  
inputSchema: {  
type: "object",  
properties: {  
productId: { type: "string" },  
quantity: { type: "number" }  
},  
required: ["productId"]  
},  
async execute({ productId, quantity }) {  
await addToCart(productId, quantity);  
return `Added ${quantity} to the cart`;  
}  
});  
`

There are four parts, and only one of them is new work.

The name is what the agent calls. The description is written in plain English, because a language model reads it to decide whether this is the right action. The schema says which inputs are valid, so bad arguments never reach your code.

The last part is the function that runs. It calls addToCart, the same function already sitting behind your own button, so you are not building a second version of your product for agents. You are pointing at the one you have.

If the thing you want to expose is already a form, you write no JavaScript at all. You add two attributes to the form markup already sitting in your HTML.

`<form toolname="search_flights"  
tooldescription="Search available flights between two cities">  
<input name="from">  
<input name="to">  
<button type="submit">Search</button>  
</form>`

The browser reads the form, works out that it takes a from and a to, and builds the schema itself.

#### How to try this?

A site that tells an agent what it can do gets cleaner, more reliable results than a site that makes the agent guess from pixels.

It is still early. One browser family has shipped it, the standard is not final, and only the browser’s own agent calls these tools today.

The cost of trying is close to nothing. If you own a site, the cheapest place to start is a form you already have. You add the two attributes, open the page in a browser that supports the trial, and watch an agent use it.

[**Read the official docs here →**](<https://developer.chrome.com/docs/ai/webmcp>)

The illustration below is a summary of how agents access web apps today.

![](https://substackcdn.com/image/fetch/$s_!HWvk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9b79f01f-df42-4bc6-9ad1-cf8f6789d25a_680x620.png)   
---
