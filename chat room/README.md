# net_prog_hw3
A chating server
操作：

  client 指令：
   
    connect IP port username  與server連線 127.0.0.1 8700 設定好了

    chat username "messege"   傳訊息給username  username 可以不只一個人

    bye  中斷連線

實做：
  利用share memory 在process之間共享記憶體
  然後在以signal告知 哪個process 去拿記憶體的資料
  
提醒自己的問題：  ```不要改變數只改一部分 全部都要一起改```
