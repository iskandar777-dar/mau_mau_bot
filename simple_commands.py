#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from telegram import ParseMode
from telegram.ext import CommandHandler

from user_setting import UserSetting
from utils import send_async
from shared_vars import dispatcher
from internationalization import _, user_locale

@user_locale
def help_handler(bot, update):
    """Handler for the /help command"""
    help_text = _("Follow these steps:\n\n"
"1. Tambahkan bot ini ke grup\n"
      "2. Di grup, mulai permainan baru dengan /baru atau bergabung dengan yang sudah"
      " menjalankan game dengan /bergabung\n"
      "3. Setelah setidaknya dua pemain bergabung, mulailah permainan dengan"
      " /mulai\n"
      "4. Ketik <code>@unobot</code> ke dalam kotak obrolan Anda dan tekan "
      "<b>spasi</b>, atau klik teks <code>via @unobot</code> "
      "di sebelah pesan. Anda akan melihat kartu Anda (beberapa berwarna abu-abu),"
      "ada opsi tambahan seperti menggambar, dan <b>?</b> untuk melihat "
      "status permainan saat ini. <b>Kartu berwarna abu-abu</b> adalah milik Anda "
      "<b>tidak bisa bermain</b> saat ini. Ketuk salah satu opsi untuk mengeksekusi "
      "tindakan yang dipilih.\n"
      “Pemain dapat bergabung dalam permainan kapan saja. Untuk keluar dari permainan,”
      “gunakan /leave. Jika pemain membutuhkan waktu lebih dari 90 detik untuk bermain,”
      "Anda dapat menggunakan /skip untuk melewati pemain itu. Gunakan /notify_me untuk "
      "menerima pesan pribadi saat game baru dimulai.\n\n"
      "<b>Bahasa</b> dan setelan lainnya: /settings\n"
      "Perintah lain (hanya pembuat game):\n"
      "/ tutup - Tutup lobi\n"
      "/ buka - Lobi terbuka\n"
      "/kill - Hentikan permainan\n"
      "/ kick - Pilih pemain yang akan ditendang"
      "dengan membalasnya\n"
      "/enable_translations - Terjemahkan teks yang relevan ke dalam semua "
      "bahasa yang digunakan dalam game\n"
      "/disable_translations - Gunakan bahasa Inggris untuk teks tersebut\n\n"
      "<b>Eksperimental:</b> Bermain dalam beberapa grup sekaligus. "
      "Tekan tombol <code>Game saat ini: ...</code> dan pilih "
      "grup tempat Anda ingin bermain kartu.\n")

    send_async(bot, update.message.chat_id, text=help_text,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@user_locale
def modes(bot, update):
    """Handler for the /help command"""
    modes_explanation = _("Bot UNO ini memiliki empat mode permainan: Klasik, Sanic, Liar, dan Teks.\n\n"
      " 🎻 Mode Klasik menggunakan dek UNO konvensional dan tidak ada lompatan otomatis.\n"
      " 🚀 Mode Sanic menggunakan dek UNO konvensional dan bot secara otomatis melewatkan pemain jika dia terlalu lama memainkan gilirannya\n"
      " 🐉 Mode Liar menggunakan dek dengan lebih banyak kartu khusus, lebih sedikit variasi angka, dan tidak ada lompatan otomatis.\n"
      " ✍️ Mode Teks menggunakan dek UNO konvensional tetapi alih-alih stiker, mode ini menggunakan teks.\n\n"
      “Untuk mengubah mode game, GAME CREATOR harus mengetikkan nickname bot dan spasi,”
      "seperti saat memainkan kartu, dan semua opsi mode permainan akan muncul.")
    
    send_async(bot, update.message.chat_id, text=modes_explanation,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)



@user_locale
def stats(bot, update):
    user = update.message.from_user
    us = UserSetting.get(id=user.id)
    if not us or not us.stats:
        send_async(bot, update.message.chat_id,
                   text=_("Anda tidak mengaktifkan statistik. Gunakan /pengaturan di "
                          "obrolan pribadi dengan bot untuk mengaktifkannya."))
    else:
        stats_text = list()

        n = us.games_played
        stats_text.append(
            _("{number} permainan yang dimainkan",
              "{number} permainan yang dimainkan",
              n).format(number=n)
        )

        n = us.first_places
        m = round((us.first_places / us.games_played) * 100) if us.games_played else 0
        stats_text.append(
            _("{number} tempat pertama ({percent}%)",
              "{number} tempat pertama ({percent}%)",
              n).format(number=n, percent=m)
        )

        n = us.cards_played
        stats_text.append(
            _("{number} kartu dimainkan",
              "{number} kartu dimainkan",
              n).format(number=n)
        )

        send_async(bot, update.message.chat_id,
                   text='\n'.join(stats_text))


def register():
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('stats', stats))
    dispatcher.add_handler(CommandHandler('modes', modes))
