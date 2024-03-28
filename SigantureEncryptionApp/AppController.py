import customtkinter as ctk
import Frames as fr
import Scripts as Scripts


class AppController(ctk.CTk):
    """
    A class used to control the application.

    ...

    Attributes
    ----------
    width_ : int
        The width of the application window.
    height_ : int
        The height of the application window.
    current_ : any
        The current frame of the application.
    frames_ : dict
        A dictionary to store the frames of the application.
    text_ : str
        A string to store text.

    Methods
    -------
    __init__():
        Initializes the application.
    sign_document_choosen():
        Checks if there is any external storage connected to the system and finds .pem files.
    set_frame(frame_name: any, *args):
        Sets the current frame of the application.
    encrypt_key(name: str):
        Prints the name of the key.
    handle_pin_entry(pin: str, path: str):
        Handles the pin entry.
    select_file_to_sign():
        Handles selecting file to sign.
    """

    width_ = 800
    height_ = 600
    current_ = None
    frames_ = {}
    text_ = ""

    def __init__(self):
        """
        Constructs all the necessary attributes for the AppController object.
        """
        super().__init__()

        self.title("Singature Encryption App")
        self.geometry(f"{self.width_}x{self.height_}")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        self.set_frame(fr.HomeFrame)
        self.rsa_key = None

    def sign_document_choosen(self):
        """
        Checks if there is any external storage connected to the system and finds .pem files.
        If storage is found, sets the FoundPendriveFrame as the current frame.
        If no storage is found, sets the NoPendriveFrame as the current frame.
        """
        storage = Scripts.check_external_storage()
        if storage is not None:
            pems = Scripts.find_pem_files(storage)
            self.set_frame(fr.FoundPendriveFrame, storage, pems)
        else:
            self.set_frame(fr.NoPendriveFrame)

    def set_frame(self, frame_name, *args):
        """
        Sets the current frame of the application.

        Parameters
        ----------
            frame_name : any
                The name of the frame to be set as the current frame.
            *args : list
                The arguments to be passed to the frame constructor.
        """
        if self.current_ is not None:
            self.current_.pack_forget()
        self.current_ = frame_name(self, self, *args)
        self.current_.pack(expand=True, fill="both")

    def decrypt_key(self, path):
        """
        Switches frame to pin entering.

        Parameters
        ----------
            path : str
                Path to the key.
        """
        self.set_frame(fr.PinEntryFrame, path, False)

    def handle_pin_entry(self, pin, path):
        """
        Handles the pin entry.
        If key is correct, sets the SelectFileToSignFrame as the current frame.
        If isn't correct, sets the PinEntryFrame with flag signalising wrong pin as the current frame.
        """
        try:
            key = Scripts.decrypt_RSA_key(pin, path)
            if key is not None:
                print(key.export_key().decode())
                self.rsa_key = key
                self.text_ = key
                self.set_frame(fr.SelectFileToSignFrame, None, False)
            else:
                print("Error decrypting key")
                pass
        except ValueError:
            self.set_frame(fr.PinEntryFrame, path, True)


    def select_file_to_sign(self):
        """
        Handles selecting file to sign
        If the extension of file is correct, sets SelectFileToSignFrame with adequate parameters:
            SelectFileToSignFrame(filePath=path, isExtensionValid=True)
        And if otherwise with arguments:
            SelectFileToSignFrame(filePath=path, isExtensionValid=False)
        """
        filename = ctk.filedialog.askopenfilename()

        isExtensionValid = Scripts.is_file_valid_to_sign(filename)
        self.set_frame(fr.SelectFileToSignFrame, filename, isExtensionValid)


    def sign_the_file(self, file_path):
        """
        Handles SIGN operation. Set
        """
        signature = Scripts.sign_file(file_path, self.rsa_key)
        self.set_frame(fr.FileSignedFrame, signature)

