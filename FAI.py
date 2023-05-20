# -----------------------------

#   DIRECTED BY FLATIOS INC

#   GITHUB: https://github.com/Flatios/FAI-PROJECT
#   GIT - LICENSE: https://github.com/Flatios/FAI-PROJECT/blob/master/LICENSE

#   Made By Hakan Kaygusuz
#   Contact Hakan Kaygusuz - hakankaygusuzone@gmail.com

# Information: Enter your FKEY below (key is taken from the site)

FKEY = "hakankgs"

# ----------------------------- 


# Libraries
import os, time, json, random as RA, pyfiglet, playsound

# Internet Libraries
from requests import request as Rrequest, get as Rget, ConnectionError as RConnectionError
from gtts import gTTS
from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError


# Variables
town = "çarşamba"
city = "samsun"
country = "tr"

# Asistant Settings
Asistant_Gender = "FEMALE"
Asistant_Name = "asistan"


class TTS_AND_STT:
    TTS_file = 'Speech.mp3'
    def speak(string): 
        if not string is None: 
            print(f"Asistant: {string}")
            if Asistant_Gender == "FEMALE": tts = gTTS(text=string, lang='tr', slow=False); 
            tts.save(TTS_AND_STT.TTS_file); FAI.FPlayerPlay(MediaPath=TTS_AND_STT.TTS_file, RemoveFile=True); 
            if Asistant_Gender == "MALE": print("Desteklenmiyor")

    def recognize_STT():
        r = Recognizer()
        with Microphone() as source: audio = r.listen(source); r.adjust_for_ambient_noise(source)
        try: Speech = r.recognize_google(audio,show_all=False ,language='tr-TR'); print(f"User: {Speech}")
        except UnknownValueError: TTS_AND_STT.speak("anlamadım.")
        except RequestError as e: TTS_AND_STT.speak("Ses tanıma servisi çalışmıyor; {0}".format(e))
        else: STT = Speech.lower(); return STT
        
class CMD_SERVER:
    def Server(API):
        if API == "FAI" or API == "FAPI": url = f"http://localhost:5000/api?fkey={FKEY}&api={API}"
        else: url = f"http://localhost:5000/api?fkey={FKEY}&api={API}&city={city}&town={town}"
        response = Rrequest("GET", url); result = json.loads(response.text)
        if result['success'] == True: return result
        
    def Importer(cmd):
        items_Server = CMD_SERVER.Server('FAI')['result'][0]['Commands']
        for item in items_Server: 
            if cmd in item["command"]: 
                if item["action"] == "speak":
                    if item["text"]: TTS_AND_STT.speak(item["text"])
                    if item["func"]: 
                        Function = item["func"]
                        if Function == "Clock": times = time.strftime("%H:%M"); hour, minute = times.split(":"); hour = "12" if hour == "00" else str(int(hour) - 12) if int(hour) > 12 else hour; period = "gece" if hour == "12" else "öğleden sonra" if int(hour) > 12 else "öğleden önce"; Func = f"Saat {period} {hour} {minute}"
                        if Function == "Exiter": Func = None; exit()
                        if Function == "PlayMusic": Func = None; FAI.FPlayer(ActionAudio="MUSIC")
                        if Function == "weather": w_Server = CMD_SERVER.Server('weather')['result'][0]; w_integer = int(float(w_Server['SICAKLIK'])); Func = f"hava {w_integer} derece, {w_Server['ACIKLAMA']}."
                        if Function == "news": n_Server = CMD_SERVER.Server('news')['result'][0]; Func = f"Haber: {n_Server['name']}, Ayrıntı: {n_Server['description']}."
                        if Function == "pod": p_Server = CMD_SERVER.Server('pod')['result'][0]; address = p_Server['address'].lower().replace("i", "ı"); Func = f"eczane adı: {p_Server['name'].lower()}, adresi: {address}."
                        if not Func == None: TTS_AND_STT.speak(Func)

class FAI:
    def FPlayer(MFN=None, AFP=None, ActionAudio=None): 
        if ActionAudio == "AUDIO": print(f"FPlayer Playing: {MFN}"); FAI.FPlayerPlay(MediaPath = AFP, RemoveFile=False) 
        if ActionAudio == "MUSIC": randarray = ['SRC/Audios/Musics/RAP/EMINEM.mp3', 'SRC/Audios/Musics/PHONK/LXAES.mp3']; rand = RA.choice(randarray); FAI.FPlayerPlay(MediaPath=rand, RemoveFile=False)
    def FPlayerPlay(MediaPath, RemoveFile):
        if os.name == "nt": playsound.playsound(MediaPath)
        if os.name == "posix": os.system("mpg321 " + MediaPath)
        if RemoveFile: os.remove(MediaPath) 
    def FAI_ASISTANT():
        voice = TTS_AND_STT.recognize_STT() 
        if not voice is None: 
            if Asistant_Name in voice: 
                if voice.strip().split()[-1] != Asistant_Name: 
                    space_after = voice.split(" ", 1)[1]; CMD_SERVER.Importer(cmd=space_after); 
                else: FAI.FPlayerPlay(MediaPath="SRC/Audios/activate.mp3", RemoveFile=False); voices = TTS_AND_STT.recognize_STT(); CMD_SERVER.Importer(cmd=voices)

        else: print("Dediğini pek anlamadım bir daha dermisin?")
            
    def main(): 
        print("-" * 52); print("FAI STARTED"); print("-" * 52)
        while True: 
            FAI.FAI_ASISTANT()
            print("-" * 52)

class FAISTARTER:
    os.system('cls||clear')
    def Start(): 
        os.system("color 4");print(pyfiglet.figlet_format("Flatios")); YES_ARRAY = ["y", "yes", "yes sir", "evet", "yeah"]; os.system("color 6")
        confirmation_INPUT = input(f"FAI çalıştırılmasını onaylıyormusunuz Y/N: ")
        if not confirmation_INPUT == None: confirmation = False; C_INPUT = confirmation_INPUT.lower()
        if C_INPUT in YES_ARRAY: print("FAI Starting..."); confirmation = True 
        else: print("FAI Unallowed"); confirmation = False
        if confirmation:
            try: Rget("https://www.google.com/"); SERVER = False
            except RConnectionError: print("Google sunucusuna bağlanılamadı"); SERVER = False
            else: print("Google sunucusuna bağlanıldı"); SERVER = True
            if SERVER: 
                if os.path.exists("Speech.mp3"):
                    print("Eski TTS dosyası siliniyor...")
                    os.remove("Speech.mp3")
                    if not os.path.exists("Speech.mp3"): print("Successfully deleted TTS file"); FAI.main()
                    else: print("TTS Dosyası Bulundu Silinmeye çalışılırken bir hata oluştu. Manuel olarak silmeniz gerekiyor!!!")
                else: print("Eski TTS dosyası bulunmadı"); FAI.main()


FAISTARTER.Start()







