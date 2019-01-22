# 翻譯布丁

## 什麼是翻譯布丁?
Line提供了語音訊息的功能使得使用者可以不用輸入任何文字來發送訊息，不過這種訊息由於某些原因對於接收者並不是那麼便利:
1. 如果你在上課中或是開會中，你無法得知訊息的內容因為你無法重播語音訊息。
2. 儘管對於訊息發送者很便利，但對於訊息接收者來說浪費了大量的時間，因為他們要花費相同的時間重播一次來得知訊息內容。

所以翻譯布丁就此誕生，他可以幫助你把語音訊息轉成文字訊息使得方便閱讀。


<p align="center"><img src="./img/img1.png" alt="Smiley face" height="200" width="250"></p>

這名字來自於[都拉Ａ夢-翻譯蒟蒻](http://zh.doraemon.wikia.com/wiki/%E7%BF%BB%E8%AD%AF%E8%92%9F%E8%92%BB?variant=zh-tw)，因為比起蒟蒻我比較喜歡吃布丁:|

## How to Use？
這個chatbot服務目前還不公開加好友，不過我提供了source codes，所以你可以自己部署並且作出任何的修改。

一但你部署完成了，只要把這個chatbot加到任何群組就可以使用了！
<p align="center"><img src="./img/img2.png" height="350" width="250"></p>
在翻譯布丁中，你可以輸入三種訊息來開啟/關閉翻譯服務，或是查詢可使用的指令：

1. `翻譯布丁`: 查看有哪些指令可以輸入。
2. `吃下翻譯布丁`: 開啟翻譯功能。
3. `布丁消化完了`: 關閉翻譯功能。

此外，當翻譯功能開啟時，有些有趣的彩蛋在裡頭(試著發送貼圖訊息看看...?)
## Demo


## Deployment
I deploy this chatbot on [Heroku](https://dashboard.heroku.com/login) now, of course you can also deploy on your own service.



## Use Language & Packages
- Python
  - Line messaging api, flask, SpeechRecognition, pydub, ffprobe, ffmpeg

## Detail
I will write a blog to describe this project in detail...if I still remember:|
