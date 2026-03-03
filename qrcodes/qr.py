# import qrcode
# import os
# from datetime import datetime

# def generate_bot_qr(telegram_id, receipt_no):

#     # just prevent if not have this folder
#     qr_dir = "qrcodes"
#     if not os.path.exists(qr_dir):
#         os.makedirs(qr_dir)
    
#     # link to open the bot
#     bot_username = "@EzMenu_Bot"  
#     deeplink = f"https://t.me/{bot_username}"

#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=3,
#         border=2
#     )

#     qr.add_data(deeplink)
#     qr.make(fit=True)

#     #generate the qr img
#     qr_image = qr.make_image(fill_color="black", back_color="white")


#     # Save QR code
#     qr_filename = f"qr_{receipt_no}.png"
#     qr_path = os.path.join(qr_dir, qr_filename)
#     qr_image.save(qr_path)
    
#     return qr_path
