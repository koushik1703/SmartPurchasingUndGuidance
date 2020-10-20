# Smart Purchasing Und Guidance


# Introduction 

SPUG - Smart Purchasing and Guidance is a system that helps the customers to shop faster by providing comfort features.


# Component Introduction 

SPUG system phyically comprises of four components 

    i) Track - The super market is laid with the tracks for the movement of the SPUG. All the products are placed at the nodes and there can be multiple SPUG's on the grid and obstacles may be present as well.
                
    ii) SPUG - The cart with Infrared sensors in the front to detect the path, Ultrasonic to detec the obstacles, LEDs' to indicate the directions. 
                 
    iii) Central Server - It holds the data regarding the product location, count of the products and the availabe carts.              
                 
    iv) Mobile Application - Its the interface between the human being and the SPUG system. 
    
In the beginning when the user comes to the supermarket with SPUG system he has to enter the cart number which is free in the app. The server checks if the cart is free and if it is free it is allotted to the user, then next user has to enter the list of products that he desires to buy, the mobile app then contactst the server and checks if the items are avaivlable and sends the product availability list to mobile application. It sends the list to the SPUG as well. The blocking points list is sent to the SPUG. 
    
SPUG calcultes the shortest path with the help of AI Planner and actuates the LED's accordingly. SPUG updaes the coordiantes locally, when the SPUG reaches product location buzzer goes on and a QR scanner will open in the mobile application to scan the QR code of the product. Once the QR code is scanned it asks the user if he wants to buy the product, if yes then it contacts the server and reduces that products total. The SPUG gets an message when the user buys the product and it will show ddirections to the next product. This goes on till all the products are purchased and it returns to the origin. Once all the products are purchased the mobile application will show the total bill amount. 


# Architecture

![arch](https://user-images.githubusercontent.com/45932617/96632422-f5909180-1317-11eb-9a98-0950bfdd6f20.png)


# Sequence Diagram

![image](https://user-images.githubusercontent.com/45932617/96615207-48128380-1301-11eb-8acd-ff811b58bfcf.png)


# Deployment Diagram

![image](https://user-images.githubusercontent.com/45932617/96615028-14375e00-1301-11eb-8e35-263a1c6b8ca4.png)


# Conclusion

User can access the products purchased during a specific timeline with the app. 
