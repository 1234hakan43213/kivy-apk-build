import json
import os
import calendar
import webbrowser  # Linkleri açmak için
from datetime import datetime
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import TouchBehavior # Uzun basma için
from kivy.utils import platform
from kivy.clock import Clock

# Bilgisayar testi için boyut
if platform != "android":
    Window.size = (360, 680)

# --- SABİTLER ---
AYLAR = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", 
         "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
GUNLER = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

LIGLER = {
    "Dolar": 10, "Bronz": 100, "Gümüş": 1000, "Altın": 10000,
    "Platin": 100000, "Elmas": 1000000, "Mitik": 10000000,
    "Şeytani": 100000000, "Takımyıldızı": 1000000000, "Tanrısal": float('inf')
}
LIG_ISIMLERI = list(LIGLER.keys())

LIG_RENKLERI = {
    "Dolar": (0.2, 0.7, 0.2, 1), "Bronz": (0.8, 0.5, 0.2, 1),
    "Gümüş": (0.7, 0.7, 0.7, 1), "Altın": (1, 0.84, 0, 1),
    "Platin": (0.8, 0.9, 1, 1), "Elmas": (0, 0.7, 0.9, 1),
    "Mitik": (0.5, 0, 0.5, 1), "Şeytani": (0.4, 0, 0, 1),
    "Takımyıldızı": (0.1, 0.1, 0.3, 1), "Tanrısal": (1, 1, 1, 1)
}

PUAN_TAKVIM = 2
PUAN_GOREV_YAPILDI = 5
PUAN_GOREV_FAIL = -2

KV = '''
#:import hex kivy.utils.get_color_from_hex

<TakvimWidget>:
    orientation: "vertical"
    padding: "2dp"
    
    MDBoxLayout:
        size_hint_y: None
        height: "30dp"
        padding: "5dp"
        
        MDIconButton:
            icon: "chevron-left"
            theme_text_color: "Custom"
            text_color: 0.2, 0.5, 0.2, 1
            on_release: root.ay_degistir(-1)
            pos_hint: {"center_y": 0.5}
            
        MDLabel:
            id: ay_yil_label
            text: "Ocak 2025"
            halign: "center"
            font_style: "Subtitle2"
            theme_text_color: "Custom"
            text_color: 0, 0.5, 0, 1
        
        MDIconButton:
            icon: "chevron-right"
            theme_text_color: "Custom"
            text_color: 0.2, 0.5, 0.2, 1
            on_release: root.ay_degistir(1)
            pos_hint: {"center_y": 0.5}

    MDGridLayout:
        cols: 7
        size_hint_y: None
        height: "20dp"
        id: gun_isimleri_grid

    MDGridLayout:
        cols: 7
        id: takvim_grid
        spacing: "2dp"
        padding: "2dp"

# Özel Buton Sınıfı: Uzun basmayı algılamak için
<KisaYolButonu>:
    icon: "star"
    icon_size: "48sp"
    theme_text_color: "Custom"
    text_color: 0.5, 0.5, 0.5, 1 # Varsayılan gri

ScreenManager:
    GirisEkrani:
    AnaEkran:
    UygulamaSecimEkrani:

<GirisEkrani>:
    name: "giris"
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDLabel:
            text: "Hoş Geldiniz"
            halign: "center"
            pos_hint: {"center_y": 0.65}
            font_style: "H4"
        
        MDTextField:
            id: kullanici_adi
            hint_text: "Adınız Soyadınız"
            mode: "rectangle"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            size_hint_x: 0.8
        
        MDFillRoundFlatButton:
            text: "Giriş Yap"
            pos_hint: {"center_x": 0.5, "center_y": 0.35}
            size_hint_x: 0.5
            on_release: root.giris_yap()

<AnaEkran>:
    name: "ana"
    MDFloatLayout:
        md_bg_color: 0.96, 0.96, 0.96, 1

        # 1. SOL ÜST: Profil
        MDCard:
            id: profil_karti
            size_hint: None, None
            size: "120dp", "120dp"
            radius: [60]
            pos_hint: {"x": 0.03, "top": 0.97}
            elevation: 4
            md_bg_color: 0.2, 0.7, 0.2, 1
            
            MDFloatLayout:
                MDCard:
                    radius: [60]
                    md_bg_color: 0, 0, 0, 0.1 
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    size_hint: 1, 1

                MDLabel:
                    id: kullanici_adi_label
                    text: "Ad Soyad"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    font_style: "Subtitle1"
                    bold: True
                    pos_hint: {"center_x": 0.5, "center_y": 0.65}
                
                MDLabel:
                    id: lig_label
                    text: "Dolar Ligi"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.9
                    font_style: "Body2"
                    pos_hint: {"center_x": 0.5, "center_y": 0.45}
                    
                MDLabel:
                    id: puan_label
                    text: "0 Puan"
                    halign: "center"
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.8
                    pos_hint: {"center_x": 0.5, "center_y": 0.3}

        # 2. SAĞ ÜST: Takvim
        MDCard:
            size_hint: 0.55, 0.35
            pos_hint: {"right": 0.98, "top": 0.97}
            radius: [15]
            elevation: 3
            padding: "5dp"
            md_bg_color: 1, 1, 1, 1
            
            TakvimWidget:
                id: ozel_takvim

        # 3. ORTA: Müzik
        MDCard:
            size_hint: 0.9, 0.1
            pos_hint: {"center_x": 0.5, "top": 0.58}
            radius: [10]
            md_bg_color: 0.1, 0.1, 0.1, 1
            elevation: 4
            padding: "10dp"
            
            MDFloatLayout:
                MDIcon:
                    icon: "spotify"
                    theme_text_color: "Custom"
                    text_color: 0.11, 0.72, 0.32, 1
                    pos_hint: {"x": 0.02, "center_y": 0.5}
                MDLabel:
                    text: "Müzik Kontrol"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    pos_hint: {"x": 0.15, "center_y": 0.5}
                    font_style: "Subtitle2"
                MDIconButton:
                    icon: "play-pause"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    pos_hint: {"right": 0.98, "center_y": 0.5}
                    on_release: app.muzik_kontrol()

        # 4. SOL ALT: Görevler
        MDCard:
            size_hint: 0.65, 0.42
            pos_hint: {"x": 0.03, "bottom": 0.02}
            radius: [20]
            elevation: 3
            orientation: "vertical"
            md_bg_color: 1, 1, 1, 1
            
            MDTopAppBar:
                title: "Görevler"
                elevation: 0
                title_color: 0,0,0,1
                right_action_items: [["plus", lambda x: app.not_ekle_dialog()]]
                md_bg_color: 0,0,0,0
                specific_text_color: 0.2, 0.2, 0.2, 1
            
            MDScrollView:
                MDList:
                    id: todo_listesi
                    padding: "10dp"

        # 5. SAĞ ALT: Akıllı Kısayollar
        MDBoxLayout:
            orientation: "vertical"
            adaptive_size: True
            pos_hint: {"right": 0.95, "bottom": 0.05}
            spacing: "15dp"

            KisaYolButonu:
                id: btn_kisayol_1
                on_release: app.kisayol_tiklandi("1")
                # Uzun basma davranışı Python tarafında tanımlandı

            KisaYolButonu:
                id: btn_kisayol_2
                on_release: app.kisayol_tiklandi("2")

            KisaYolButonu:
                id: btn_kisayol_3
                on_release: app.kisayol_tiklandi("3")

<UygulamaSecimEkrani>:
    name: "uygulama_secim"
    MDFloatLayout:
        md_bg_color: 0.1, 0.1, 0.1, 1 # Siyah arka plan (Resimdeki gibi)
        
        MDBoxLayout:
            orientation: "vertical"
            
            MDTopAppBar:
                title: "Uygulamaları Seç"
                md_bg_color: 0.1, 0.1, 0.1, 1
                specific_text_color: 1, 1, 1, 1
                elevation: 0
                left_action_items: [["arrow-left", lambda x: root.geri_don()]]

            MDScrollView:
                MDList:
                    id: uygulama_listesi
'''

# --- CUSTOM BUTTON WITH LONG PRESS ---
class KisaYolButonu(MDIconButton, TouchBehavior):
    def on_long_touch(self, touch, *args):
        # Butona uzun basıldığında silme onayı
        app = MDApp.get_running_app()
        # ID'yi bul (btn_kisayol_1 -> 1)
        slot_id = ""
        for k, v in app.root.get_screen("ana").ids.items():
            if v == self:
                slot_id = k.split("_")[-1]
                break
        
        if slot_id:
            app.kisayol_sil_dialog(slot_id)
        return True

class TakvimWidget(MDBoxLayout):
    simdiki_yil = datetime.now().year
    simdiki_ay = datetime.now().month

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.baslangic_ayarlari, 0.1)

    def baslangic_ayarlari(self, dt):
        grid_isim = self.ids.gun_isimleri_grid
        for gun in GUNLER:
            lbl = MDLabel(text=gun, halign="center", font_style="Caption", theme_text_color="Secondary")
            grid_isim.add_widget(lbl)
        self.takvimi_ciz()

    def ay_degistir(self, yon):
        self.simdiki_ay += yon
        if self.simdiki_ay > 12:
            self.simdiki_ay = 1
            self.simdiki_yil += 1
        elif self.simdiki_ay < 1:
            self.simdiki_ay = 12
            self.simdiki_yil -= 1
        self.takvimi_ciz()

    def takvimi_ciz(self):
        self.ids.ay_yil_label.text = f"{AYLAR[self.simdiki_ay]} {self.simdiki_yil}"
        grid = self.ids.takvim_grid
        grid.clear_widgets()
        
        ilk_gun_indeks, toplam_gun = calendar.monthrange(self.simdiki_yil, self.simdiki_ay)
        
        for _ in range(ilk_gun_indeks):
            grid.add_widget(MDLabel(text=""))
            
        app = MDApp.get_running_app()
        
        for i in range(1, toplam_gun + 1):
            btn = MDFlatButton(
                text=str(i),
                size_hint=(None, None),
                size=("30dp", "30dp"),
                font_size="12sp",
                theme_text_color="Custom",
                text_color=(0.2, 0.2, 0.2, 1),
            )
            btn.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            btn.bind(on_release=self.gun_sec)
            
            tam_tarih = f"{i} {AYLAR[self.simdiki_ay]} {self.simdiki_yil}"
            if tam_tarih in app.secili_tarihler:
                self.stili_secili_yap(btn)
            
            btn.size_hint = (1, 1)
            grid.add_widget(btn)

    def gun_sec(self, instance):
        app = MDApp.get_running_app()
        secilen_gun = instance.text
        tam_tarih = f"{secilen_gun} {AYLAR[self.simdiki_ay]} {self.simdiki_yil}"
        
        if tam_tarih in app.secili_tarihler:
            app.secili_tarihler.remove(tam_tarih)
            self.stili_normale_don(instance)
            app.puan_degistir(-PUAN_TAKVIM)
        else:
            app.secili_tarihler.append(tam_tarih)
            self.stili_secili_yap(instance)
            app.puan_degistir(PUAN_TAKVIM)

    def stili_secili_yap(self, btn):
        btn.md_bg_color = (0, 0.7, 0, 1)
        btn.text_color = (1, 1, 1, 1)
        btn.rounded_button = True
        btn.radius = [25]

    def stili_normale_don(self, btn):
        btn.md_bg_color = (0, 0, 0, 0)
        btn.text_color = (0.2, 0.2, 0.2, 1)
        btn.radius = [0]

class GirisEkrani(MDScreen):
    def giris_yap(self):
        ad = self.ids.kullanici_adi.text.strip()
        if ad:
            app = MDApp.get_running_app()
            app.kullanici_adi = ad
            app.verileri_kaydet()
            self.manager.current = "ana"
            app.ana_ekran_bilgilerini_guncelle()

class AnaEkran(MDScreen):
    pass

class UygulamaSecimEkrani(MDScreen):
    def geri_don(self):
        MDApp.get_running_app().root.current = "ana"

class BenimUygulamam(MDApp):
    kullanici_adi = ""
    gorevler = []
    secili_tarihler = []
    mevcut_puan = 0
    kisayollar = {} # {"1": {"type": "app", "val": "com.x"}, "2": {"type": "link", "val": "http"}}
    
    dialog = None
    veri_dosyasi = "uygulama_verisi_v4.json"
    aktif_slot_secimi = None # Hangi yıldıza atama yapıyoruz?

    def build(self):
        self.theme_cls.primary_palette = "Green"
        calendar.setfirstweekday(0) 
        return Builder.load_string(KV)

    def on_start(self):
        self.verileri_yukle()
        if self.kullanici_adi:
            self.root.current = "ana"
            self.ana_ekran_bilgilerini_guncelle()
            for gorev in self.gorevler:
                self.ekrana_gorev_widget_ekle(gorev)
            self.yildizlari_guncelle()

    # --- KISAYOL SİSTEMİ ---
    
    def kisayol_tiklandi(self, slot_id):
        # Eğer slot boşsa -> Atama yap
        if slot_id not in self.kisayollar:
            self.aktif_slot_secimi = slot_id
            self.tur_secim_dialog()
        else:
            # Slot dolu -> Çalıştır
            data = self.kisayollar[slot_id]
            tur = data["type"]
            deger = data["val"]
            
            if tur == "link":
                webbrowser.open(deger)
            elif tur == "app":
                self.uygulama_ac(deger)

    def tur_secim_dialog(self):
        # Kullanıcıya sor: Link mi, Uygulama mı?
        if self.dialog: self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Kısayol Türü Seç",
            text="Bu yıldıza ne atamak istersiniz?",
            buttons=[
                MDFlatButton(text="LİNK (URL)", on_release=lambda x: self.link_giris_ac()),
                MDFillRoundFlatButton(text="UYGULAMA", on_release=lambda x: self.uygulama_listesini_yukle()),
            ],
        )
        self.dialog.open()

    def link_giris_ac(self):
        self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Link Ekle",
            type="custom",
            content_cls=MDTextField(hint_text="https://www.google.com", id="link_input"),
            buttons=[
                MDFlatButton(text="İPTAL", on_release=self.dialog_kapat),
                MDFillRoundFlatButton(text="KAYDET", on_release=self.link_kaydet)
            ],
        )
        self.dialog.open()

    def link_kaydet(self, obj):
        link = self.dialog.content_cls.text
        if link:
            # Başına https koymamışsa ekleyelim
            if not link.startswith("http"):
                link = "https://" + link
            
            self.kisayollar[self.aktif_slot_secimi] = {"type": "link", "val": link}
            self.verileri_kaydet()
            self.yildizlari_guncelle()
        self.dialog.dismiss()

    def uygulama_listesini_yukle(self):
        self.dialog.dismiss()
        
        # Uygulama seçim ekranına geç
        self.root.current = "uygulama_secim"
        liste_widget = self.root.get_screen("uygulama_secim").ids.uygulama_listesi
        liste_widget.clear_widgets()
        
        uygulamalar = []
        
        # --- ANDROID TARAFI ---
        if platform == "android":
            try:
                from jnius import autoclass
                
                # Gerekli Android sınıflarını çağır
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                
                context = PythonActivity.mActivity
                pm = context.getPackageManager()
                
                # Sadece "BAŞLATILABİLİR" (Launcher) aktiviteleri ara
                # Bu işlem sistem servislerini ve arkaplan dosyalarını gizler.
                intent = Intent(Intent.ACTION_MAIN, None)
                intent.addCategory(Intent.CATEGORY_LAUNCHER)
                
                # Listeyi çek
                apps_list = pm.queryIntentActivities(intent, 0)
                
                # Listeyi döngüye sok
                for resolve_info in apps_list.toArray():
                    # Uygulama adı
                    app_name = resolve_info.loadLabel(pm).toString()
                    # Paket adı (com.instagram.android gibi)
                    pkg_name = resolve_info.activityInfo.packageName
                    
                    # Kendimizi listeye eklemeyelim :)
                    if pkg_name != context.getPackageName():
                        uygulamalar.append((app_name, pkg_name))
                
                # İsme göre A'dan Z'ye sırala
                uygulamalar.sort(key=lambda x: x[0].lower())
                
            except Exception as e:
                print("Hata:", e)
                # Hata durumunda test verisi göster
                uygulamalar = [("Hata Oluştu", ""), ("Ayarlar", "com.android.settings")]

        # --- PC (TEST) TARAFI ---
        else:
            # PC'deysen sadece bu sahte listeyi görürsün.
            # Tıkladığında konsola "PC Modu: ... açılıyor" yazar.
            uygulamalar = [
                ("Facebook (Test)", "com.facebook.katana"),
                ("Instagram (Test)", "com.instagram.android"), 
                ("WhatsApp (Test)", "com.whatsapp"), 
                ("YouTube (Test)", "com.google.android.youtube"),
                ("Ayarlar (Test)", "com.android.settings")
            ]

        # Listeyi Ekrana Bas
        for ad, paket in uygulamalar:
            # Görünüm
            item = OneLineAvatarIconListItem(text=ad, theme_text_color="Custom", text_color=(1,1,1,1))
            icon = IconLeftWidget(icon="android", theme_text_color="Custom", text_color=(0, 1, 0, 1))
            
            # Tıklama Olayı
            item.bind(on_release=lambda x, p=paket: self.uygulama_secildi(p))
            
            item.add_widget(icon)
            liste_widget.add_widget(item)

    def uygulama_secildi(self, paket_adi):
        self.kisayollar[self.aktif_slot_secimi] = {"type": "app", "val": paket_adi}
        self.verileri_kaydet()
        self.root.current = "ana"
        self.yildizlari_guncelle()

    def kisayol_sil_dialog(self, slot_id):
        if self.dialog: self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Kısayolu Sil",
            text="Bu yıldıza atanan kısayolu kaldırmak istiyor musunuz?",
            buttons=[
                MDFlatButton(text="İPTAL", on_release=self.dialog_kapat),
                MDFillRoundFlatButton(text="SİL", on_release=lambda x: self.kisayol_sil(slot_id))
            ],
        )
        self.dialog.open()

    def kisayol_sil(self, slot_id):
        if slot_id in self.kisayollar:
            del self.kisayollar[slot_id]
            self.verileri_kaydet()
            self.yildizlari_guncelle()
        self.dialog.dismiss()

    def yildizlari_guncelle(self):
        screen = self.root.get_screen("ana")
        # 3 slotu kontrol et
        for i in range(1, 4):
            btn_id = f"btn_kisayol_{i}"
            btn = screen.ids.get(btn_id)
            if not btn: continue
            
            slot_id = str(i)
            if slot_id in self.kisayollar:
                # Doluysa Renkli Yap
                tur = self.kisayollar[slot_id]["type"]
                if tur == "app":
                    btn.text_color = (0, 0.8, 0.2, 1) # Uygulamalar Yeşil
                else:
                    btn.text_color = (0.2, 0.6, 1, 1) # Linkler Mavi
            else:
                # Boşsa Gri Yap
                btn.text_color = (0.5, 0.5, 0.5, 1)

    # --- PUAN / GÖREV / DİĞER FONKSİYONLAR (Aynı) ---
    def puan_degistir(self, miktar):
        eski_lig = self.mevcut_lig_bul()
        self.mevcut_puan += miktar
        if self.mevcut_puan < 0: self.mevcut_puan = 0
        yeni_lig = self.mevcut_lig_bul()
        if LIG_ISIMLERI.index(yeni_lig) > LIG_ISIMLERI.index(eski_lig):
            self.tebrik_dialog_ac(yeni_lig)
        self.verileri_kaydet()
        self.ana_ekran_bilgilerini_guncelle()

    def mevcut_lig_bul(self):
        for lig_adi, baraj_puan in LIGLER.items():
            if self.mevcut_puan < baraj_puan:
                return lig_adi
        return "Tanrısal"

    def tebrik_dialog_ac(self, yeni_lig):
        if self.dialog: self.dialog.dismiss()
        self.dialog = MDDialog(
            title="TEBRİKLER! 🎉",
            text=f"Lig Atladın:\n\n[b]{yeni_lig.upper()} LİGİ![/b]",
            buttons=[MDFillRoundFlatButton(text="DEVAM ET", on_release=self.dialog_kapat)],
        )
        self.dialog.open()

    def ana_ekran_bilgilerini_guncelle(self):
        screen = self.root.get_screen("ana")
        if screen and self.kullanici_adi:
            lig = self.mevcut_lig_bul()
            screen.ids.kullanici_adi_label.text = self.kullanici_adi.upper()
            screen.ids.lig_label.text = f"{lig} Ligi"
            screen.ids.puan_label.text = f"{self.mevcut_puan} Puan"
            yeni_renk = LIG_RENKLERI.get(lig, (0.2, 0.7, 0.2, 1))
            screen.ids.profil_karti.md_bg_color = yeni_renk

    def verileri_kaydet(self):
        data = {
            "ad": self.kullanici_adi,
            "gorevler": self.gorevler,
            "tarihler": self.secili_tarihler,
            "puan": self.mevcut_puan,
            "kisayollar": self.kisayollar # YENİ
        }
        with open(self.veri_dosyasi, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def verileri_yukle(self):
        if os.path.exists(self.veri_dosyasi):
            with open(self.veri_dosyasi, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.kullanici_adi = data.get("ad", "")
                    self.gorevler = data.get("gorevler", [])
                    self.secili_tarihler = data.get("tarihler", [])
                    self.mevcut_puan = data.get("puan", 0)
                    self.kisayollar = data.get("kisayollar", {})
                except:
                    pass

    def not_ekle_dialog(self):
        if self.dialog: self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Yeni Görev",
            type="custom",
            content_cls=MDTextField(hint_text="Görev yaz...", id="yeni_gorev"),
            buttons=[
                MDFlatButton(text="İPTAL", on_release=self.dialog_kapat),
                MDFillRoundFlatButton(text="EKLE", on_release=self.gorev_kaydet)
            ],
        )
        self.dialog.open()

    def dialog_kapat(self, obj):
        if self.dialog: self.dialog.dismiss()

    def gorev_kaydet(self, obj):
        textfield = self.dialog.content_cls
        metin = textfield.text
        if metin:
            self.gorevler.append(metin)
            self.ekrana_gorev_widget_ekle(metin)
            self.verileri_kaydet()
        self.dialog_kapat(obj)

    def ekrana_gorev_widget_ekle(self, metin):
        screen = self.root.get_screen("ana")
        item = OneLineAvatarIconListItem(text=metin)
        icon_ok = IconLeftWidget(icon="check-circle", theme_text_color="Custom", text_color=(0, 0.7, 0, 1))
        icon_ok.bind(on_release=lambda x: self.gorev_tamamla(item, metin, basarili=True))
        icon_fail = IconRightWidget(icon="close-circle", theme_text_color="Custom", text_color=(0.8, 0.1, 0.1, 1))
        icon_fail.bind(on_release=lambda x: self.gorev_tamamla(item, metin, basarili=False))
        item.add_widget(icon_ok)
        item.add_widget(icon_fail)
        screen.ids.todo_listesi.add_widget(item)

    def gorev_tamamla(self, item_widget, metin, basarili):
        screen = self.root.get_screen("ana")
        screen.ids.todo_listesi.remove_widget(item_widget)
        if metin in self.gorevler:
            self.gorevler.remove(metin)
        if basarili:
            self.puan_degistir(PUAN_GOREV_YAPILDI)
        else:
            self.puan_degistir(PUAN_GOREV_FAIL)

    def muzik_kontrol(self):
        if platform == "android":
            try:
                from jnius import autoclass
                KeyEvent = autoclass('android.view.KeyEvent')
                Instrumentation = autoclass('android.app.Instrumentation')
                Instrumentation().sendKeyDownUpSync(KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE)
            except: pass
        else: print("Müzik Kontrol Edildi")

    def uygulama_ac(self, paket_adi):
        if platform == "android":
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                pm = activity.getPackageManager()
                launch_intent = pm.getLaunchIntentForPackage(paket_adi)
                if launch_intent:
                    activity.startActivity(launch_intent)
                else:
                    print("Uygulama bulunamadı")
            except Exception as e:
                print(f"Hata: {e}")
        else:
            print(f"PC Modu: {paket_adi} açılıyor simülasyonu.")

if __name__ == "__main__":
    BenimUygulamam().run()