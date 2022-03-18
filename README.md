## Location Selection Analysis for Hand Shake Beverages Store -A Case Study of Taipei City  
This project want to analyze selection for hand-shake beverages stores in Taipei by open government data  

### Analysis and Report
Analysis code and general description (English): Please view the [website](https://tim-hansheng-huang.github.io/LocationSelectionProject/LocationSelection_Analysis.html)  
Detailed report (Chinese): "[手搖飲料店設點選址的分析研究](https://github.com/Tim-HanSheng-Huang/LocationSelectionProject/blob/main/%E6%89%8B%E6%90%96%E9%A3%B2%E6%96%99%E5%BA%97%E8%A8%AD%E9%BB%9E%E9%81%B8%E5%9D%80%E7%9A%84%E5%88%86%E6%9E%90%E7%A0%94%E7%A9%B6.pdf)"  

### System Implementation
This project not only provide a report, but also implement a tool that help beverage companies do the location selection according to relative information. After inputing a Chinese address in Taipei, users would get a predicted success probability for the address.  
The image below is the interface of the system. [Here](https://youtu.be/O-T8adiqFRU) is the system demo video.   
  
![image](https://github.com/Tim-HanSheng-Huang/LocationSelectionProject/blob/main/interface.png)

### Download the system
The system is a python application and  was packaged into a single folder, which can be downloaded [here](https://drive.google.com/drive/folders/19RO0BDYo3bNgDFYa31kFZ3YahBSVRWbF). Users just need to download the whole folder and click the execution file "LocationSelection_System.exe". Then, users can input the address and get the predicted outcome.  
Because the system need to get the latitude and longitude of the address by web crawler, this system need to execute with internet and Chrome (version 99). 
