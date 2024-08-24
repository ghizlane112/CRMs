# test_import.py
try:
    from xhtml2pdf import pisa
    print("xhtml2pdf importé avec succès")
except ImportError as e:
    print(f"Erreur d'importation : {e}")
