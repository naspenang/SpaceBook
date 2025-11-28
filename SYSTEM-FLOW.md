# 🔄 System Flow

This explains how bookings move through SpaceBook.

---

## 1. Login
User signs in through Google  
→ System verifies email  
→ User enters dashboard

---

## 2. Branch Selection
User picks a library branch  
→ System loads spaces for that branch

---

## 3. Space Browsing
User sees room list  
→ Chooses a space  
→ Opens availability page

---

## 4. Booking Request
User enters:
- Date  
- Start time  
- End time  

System checks:
- Overlaps
- Opening hours
- Closure dates
- Buffer time

If OK:
- Booking is created

---

## 5. Approval Stage (If Needed)
If room needs approval:
- Booking goes “Pending”
- Librarian reviews
- Approves or rejects

---

## 6. Notifications
Email sent for:
- Booking created
- Booking approved
- Booking rejected
- Booking cancelled

---

## 7. Payment Stage
If required:
- PaymentLog created
- Bank updates status

---

## 8. Reporting
Admins & UiTM management can:
- Filter dates
- View charts
- Check totals & averages

