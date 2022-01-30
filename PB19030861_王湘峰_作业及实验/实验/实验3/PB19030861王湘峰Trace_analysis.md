<center><font size=7>
    <b>
    802.11 Trace Analysis
</center>


### PB19030861 王湘峰

#### 1.What are the SSIDs of the two APs that are issuing most of the beacon frames in this trace? 

发送信标帧最多的AP是 **30 Munroe St** 和 **linksys12** .

(下图为过滤出了所有beacon frame，可以看到最多的SSID为**30 Munroe St**)

![1](D:\干点正事\大三上\计网\实验3\1.1.png)

（下图为去除掉**30 Munroe St**后的beacon frame信息，易知第二多的AP是**linksys12**）

![1.2](D:\干点正事\大三上\计网\实验3\1.2.png)

#### 2.What are the three addresses in the Beacon frame from the two APs respectively. 

| Address/AP |   30 Munroe St    |     linksys12     |
| :--------: | :---------------: | :---------------: |
|  address1  | ff:ff:ff:ff:ff:ff | ff:ff:ff:ff:ff:ff |
|  address2  | 00:16:b6:f7:1d:51 | 00:06:25:67:22:94 |
|  address3  | 00:16:b6:f7:1d:51 | 00:06:25:67:22:94 |

![2.1](D:\干点正事\大三上\计网\实验3\2.1.png)

![2.2](D:\干点正事\大三上\计网\实验3\2.2.png)

#### 3.How many APs the wireless laptop has received Beacon frames from? List their MAC addresses. Why the laptop can receive frames from an AP even though it does not associate with the AP? 

一共有3个收到信标帧的AP：30 Munroe St, linksys12, linksys_SES_24806.

|       SSID        |      Address      |
| :---------------: | :---------------: |
|   30 Munroe St    | 00:16:b6:f7:1d:51 |
|     linksys12     | 00:06:25:67:22:94 |
| linksys_SES_24806 | 00:18:39:93:b9:bb |

解释：

根据IEEE 802.11a/b/g/n 协议，每个AP每隔一定时间（几十毫秒到几秒不等）向周围的STA和AP广播beacon帧，以此让别的STA和AP与之相连接。所以收到的beacon帧是AP的广播帧。

（下图为去除主要的三个AP后得到的beacon frame，对每个帧观察发现其BSSID总是和上面三种之一重合，以此推断这些SSID其实是信号失真导致的，一共只收到了3个AP的帧）

![3](D:\干点正事\大三上\计网\实验3\3.png)

#### 4.Find the 802.11 frame containing the SYN TCP segment for this first TCP session (that downloads alice.txt). What are the three MAC addresses in the frame, which is the address for wireless laptop / AP / first-hop router? 

(表格1从上至下依次为Address1, Address2, Address3)

|    Receiver Address     |   00:16:b6:f7:1d:51   |        **AP**        |
| :---------------------: | :-------------------: | :------------------: |
| **Transmitter Address** | **00:13:02:d1:b6:4f** | **wireless laptop**  |
| **Destination Address** | **00:16:b6:f4:eb:a8** | **first-hop router** |

![4](D:\干点正事\大三上\计网\实验3\4.png)

#### 5.For the SYN-ACK segment of the first TCP session, what are the three MAC addresses in the frame, and which is the address for wireless laptop / AP / first-hop router? 

(表格1从上至下依次为Address1, Address2, Address3)

|    Receiver Address     | **00:13:02:d1:b6:4f** |   wireless laptop    |
| :---------------------: | :-------------------: | :------------------: |
| **Transmitter Address** | **00:16:b6:f7:1d:51** |        **AP**        |
|   **Source Address**    | **00:16:b6:f4:eb:a8** | **first-hop router** |

![5](D:\干点正事\大三上\计网\实验3\5.png)

#### 6.For the above mentioned SYN-ACK segment, is the sender MAC address corresponds to the web server’s IP address? Why? 

**答：**不是的，发送端的MAC地址是AP的而非web服务器的。在数据链路层，帧的发送地址与接收地址为相邻节点的MAC地址。

#### 7.What two actions are taken (i.e., frames are sent) by the host in the trace just after *t=49*, to end the association with the *30 Munroe St* AP? 

**1. ** Release DHCP

**2.**  Deauthentication

![7](D:\干点正事\大三上\计网\实验3\7.png)

#### 8.Can you capture a similar trace? Why or why not? 

由于本人的电脑网卡不支持monitor功能，无法捕捉802.11帧，故不能复现该实验。
