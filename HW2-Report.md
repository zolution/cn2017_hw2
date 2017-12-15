# Computer Network HW2

<b>Homework Topic: Retransmission & Congest Control</b><br>
National Taiwan University<br>
CSIE3510 Class 01, 2017 Fall<br>
Written By: B04902077 Wei-Hsuan Chiang

## Execution

- Platform: Python 3.6.3

- Sender:

  ```sh
  $ python sender.py <filename_to_send>
  ```

- Agent:

  ```sh
  $ python agent.py <loss_rate>
  ```

- Receiver

  ```Sh
  $ python receiver.py <filename_to_save> 
  ```

- If the IP and port configuration parameters are given in the arguments, then the execution command will be too complex since all 3 IP-Port pairs should be given to all of them. As a result, in my implementation, all these information are hard-coded in the python script, but it can be easily modified.

## Program Structure

- Overall: As the spec slide page 27 suggested

  ![Screen Shot 2017-12-15 at 9.40.22 PM](/Users/wchiang/Desktop/Screen Shot 2017-12-15 at 9.40.22 PM.png)

- Sender/Agent/Receiver:
  <div align=center>

  <img src="/Users/wchiang/Desktop/Picture1.png" width="60%">

  </div>

## Difficulties and Solutions

- Python Version Issues

  At first, I used python2 to implement this homework, and `pickle` is applied to encode and decode the packets. However, since `pickle` acts differently in python2 and python3, and it cannot normally dump the byte string, it bothered me for a long time.

  <b>Solution:</b> Change to Python3

- Timeout Issues in sender

  At first I used socket.settimeout() to deal with the timeout ack in sender. However, after some discussion and confirmation, this does not meet the spec requirement. Finally, I applied signal `SIGALRM`to deal with the timeout part.

  <b>Solution:</b> Implement signal and set alarm in python