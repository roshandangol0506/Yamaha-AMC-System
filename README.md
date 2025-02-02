# 🏍️ Yamaha AMC (Annual Maintenance System)

A web-based system designed for Yamaha service centers to streamline **bike servicing, user management, and card-based service tracking**. It ensures efficient service approvals, automated email notifications, and renewal management.  

## 🚀 Features  

Admin |||--- manages ---||| Customer

Admin |||--- approves ---||| Bike Service

Admin |||--- updates ---||| Customer Service Statements

Admin |||--- sends renewal alert to ---||| Customer (when services = 0)

Customer |||--- owns ---||| Bike

Customer |||--- swipes card for ---||| Service Request

Customer |||--- receives email from ---||| AMC System (after service)

Service Request |||--- contains ---||| Customer Details

Service Request |||--- waits for approval from ---||| Admin

Service Request |||--- reduces ---||| Remaining Services by 1 (on approval)

Bike |||--- undergoes ---||| Servicing

Bike |||--- linked with ---||| Customer

Customer |||--- needs renewal when ---||| Remaining Services = 0


### 👤 Admin  
- Add, manage, and update customer details.  
- Each customer receives **4 bike services** upon registration.  
- When a customer **swipes their card**, the system:  
  - Retrieves and displays customer details.  
  - Sends an approval request to the admin.  
- Upon admin approval:  
  - The **service count decreases by 1**.  
  - The customer receives an **email notification** confirming the service.  
- View and edit customer service statements.  
- If a customer’s **remaining services reach 0**, their status is marked **red**, and renewal is required.  

## 🛠️ Tech Stack  
- **Backend**: Django (Python)  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**: MySQL  
- **Hardware Integration**: Card-swiping device for customer authentication  
- **Email Notifications**: Automated email alerts for servicing updates  

## 📸 Screenshots  
![Screenshot 2025-02-02 160314](https://github.com/user-attachments/assets/a7b9834e-27da-4b45-9953-cf0c9dd7ac87)
![Screenshot 2025-02-02 160138](https://github.com/user-attachments/assets/c7843888-4c46-4c51-b442-b3b2ae4fe2ab)
![Screenshot 2025-02-02 160151](https://github.com/user-attachments/assets/4d093bc5-9638-476e-9af3-11720771adba)
![Screenshot 2025-02-02 160226](https://github.com/user-attachments/assets/99925ccc-687a-4af0-9d2f-1cc7e901c238)
![Screenshot 2025-02-02 160252](https://github.com/user-attachments/assets/b7b346d5-447b-4c83-b468-9b072544b73a)
 

## 🔧 Installation  

1. Clone the repository:  
   ```sh
   https://github.com/roshandangol0506/Yamaha-AMC-System.git
