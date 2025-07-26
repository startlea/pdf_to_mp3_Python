import tkinter as tk  # Import biblioteki Tkinter jako tk
from tkinter import filedialog, messagebox  # Import klas filedialog i messagebox z Tkinter
import pyttsx3  # Import biblioteki pyttsx3 do syntezy mowy
from PyPDF2 import PdfReader  # Import klasy PdfReader z biblioteki PyPDF2
import threading  # Import biblioteki threading do obsługi wątków


class PDFReaderGUI:
    def __init__(self, master):
        """Inicjalizacja okna GUI."""
        self.master = master  # Przypisanie okna głównego
        master.title("PDF Reader")  # Ustawienie tytułu okna

        # Etykieta informująca użytkownika o wyborze pliku
        self.label = tk.Label(master, text="Wybierz plik PDF:")
        self.label.pack(pady=10)  # Dodanie etykiety do okna z paddingiem w osi Y

        # Przycisk do przeglądania plików
        self.browse_button = tk.Button(master, text="Przeglądaj", command=self.browse_file)
        self.browse_button.pack(pady=5)  # Dodanie przycisku do okna z paddingiem w osi Y

        # Przycisk do odczytu PDF, początkowo wyłączony
        self.read_button = tk.Button(master, text="Czytaj PDF", command=self.read_pdf, state=tk.DISABLED)
        self.read_button.pack(pady=5)  # Dodanie przycisku do okna z paddingiem w osi Y

        self.file_path = None  # Ścieżka do wybranego pliku PDF (początkowo None)
        self.engine = pyttsx3.init()  # Inicjalizacja silnika syntezy mowy

    def browse_file(self):
        """Otwiera okno dialogowe do wyboru pliku PDF."""
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])  # Otwarcie okna dialogowego
        if self.file_path:  # Jeśli plik został wybrany
            self.label.config(text=f"Wybrano plik: {self.file_path}")  # Aktualizacja etykiety z nazwą pliku
            self.read_button.config(state=tk.NORMAL)  # Aktywacja przycisku "Czytaj PDF"
        else:  # Jeśli plik nie został wybrany
            self.label.config(text="Wybierz plik PDF:")  # Reset etykiety
            self.read_button.config(state=tk.DISABLED)  # Wyłączenie przycisku "Czytaj PDF"

    def read_pdf(self):
        """Sprawdza, czy plik został wybrany i uruchamia odczyt PDF w osobnym wątku."""
        if not self.file_path:  # Jeśli ścieżka pliku nie została ustawiona
            messagebox.showerror("Błąd", "Najpierw wybierz plik PDF.")  # Wyświetlenie komunikatu o błędzie
            return  # Przerwanie funkcji

        # Wykorzystanie wątku aby uniknąć zawieszenia GUI
        threading.Thread(target=self.process_and_read_pdf).start()

    def process_and_read_pdf(self):
        """Przetwarza plik PDF, wyodrębnia tekst, czyta go i zapisuje do pliku MP3."""
        try:  # Obsługa potencjalnych błędów
            pdfreader = PdfReader(self.file_path)  # Utworzenie obiektu PdfReader
            page_num = len(pdfreader.pages)  # Pobranie liczby stron w PDF
            text = ""  # Inicjalizacja pustego ciągu tekstowego

            for page_num in range(page_num):  # Iteracja po stronach PDF
                page = pdfreader.pages[page_num]  # Pobranie strony
                text += page.extract_text() + "\n"  # Wyodrębnienie tekstu i dodanie do ciągu

            print(text)  # Wyświetl tekst w konsoli

            self.engine.say(text)  # Przekazanie tekstu do syntezatora mowy
            self.engine.save_to_file(text, "story.mp3")  # Zapisanie mowy do pliku MP3
            self.engine.runAndWait()  # Odtworzenie mowy
            self.engine.stop()  # Zatrzymanie silnika syntezy mowy

            messagebox.showinfo("Zakończono", "Odczytywanie PDF zakończone i zapisane jako story.mp3!")  # Wyświetlenie komunikatu o zakończeniu

        except Exception as e:  # Obsługa błędów
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas odczytywania pliku PDF: {e}")  # Wyświetlenie komunikatu o błędzie


root = tk.Tk()  # Utworzenie okna głównego
gui = PDFReaderGUI(root)  # Utworzenie instancji klasy GUI
root.mainloop()  # Uruchomienie pętli zdarzeń GUI
