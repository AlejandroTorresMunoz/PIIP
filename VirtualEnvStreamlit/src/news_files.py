import os
import streamlit as st

# @st.cache_resource
def load_pdf_files():
    PATH_PDF_FILES = "../Articulos"
    
    # Crear una lista con las rutas completas de los archivos PDF
    pdf_files = [os.path.join(PATH_PDF_FILES, f) for f in os.listdir(PATH_PDF_FILES) if f.endswith('.pdf')]
    
    return pdf_files
