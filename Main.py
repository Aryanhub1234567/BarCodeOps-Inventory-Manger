#import Scanner
import Database
#from Scanner import scan_barcode
#from Database import get_product_by_barcode

#Pr1 = Database.Product("98765432100", "Wireless Mouse", 15, 299.99, "Bluetooth enabled")
#Database.insert_product(Pr1)

'''Database.insert_product(Database.Product("8901234567890", "Wireless Mouse", 25, 699, "Computer Accessory"))
Database.insert_product(Database.Product("8909876543210", "USB-C Charging Cable", 50, 299, "Mobile Accessory"))
Database.insert_product(Database.Product("8901122334455", "Bluetooth Speaker", 15, 2499, "Electronic Gadget"))
Database.insert_product(Database.Product("8909988776655", "Laptop Cooling Pad", 20, 1199, "Computer Accessory"))
Database.insert_product(Database.Product("8904433221100", "Gaming Keyboard", 12, 3499, "Computer Accessory"))
Database.insert_product(Database.Product("8905678901234", "Smartwatch Strap", 40, 499, "Mobile Accessory"))
Database.insert_product(Database.Product("8907766554433", "Power Bank 20000mAh", 18, 1699, "Electronic Gadget"))
Database.insert_product(Database.Product("8903344556677", "Wireless Earbuds", 22, 2299, "Electronic Gadget"))
Database.insert_product(Database.Product("8902211334455", "External Hard Drive 1TB", 10, 4299, "Computer Accessory"))
Database.insert_product(Database.Product("8906655443322", "Mobile Holder for Car", 35, 399, "Mobile Accessory"))
'''
'''barcode = scan_barcode()
if barcode:
    product = get_product_by_barcode(barcode)
    if product:
        print("Product Found:", product)
    else:
        print("Product not found in inventory.")
else:
    print("No barcode scanned.")'''
