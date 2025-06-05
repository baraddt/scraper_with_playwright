# from playwright.sync_api import sync_playwright
# import json


# def scrape(url: str):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(channel="chrome", headless=True)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto(url)
#         page.wait_for_timeout(6000)

#         result = {
#             "title": None,
#             "sold": None,
#             "rating": None,
#             "rating_count": None,
#             "variants": [],
#         }

#         # Ambil judul produk
#         try:
#             title_locator = page.locator(".title-v0v6fK")
#             title_locator.wait_for(timeout=5000)
#             result["title"] = title_locator.inner_text().strip()
#         except Exception as e:
#             print("Gagal mengambil judul produk:", e)

#         # Ambil rating
#         try:
#             rating_text = (
#                 page.locator("span.infoRatingScore-jSs6kd").inner_text().strip()
#             )
#             result["rating"] = float(rating_text)
#         except Exception as e:
#             print("Gagal mengambil rating:", e)

#         # Ambil rating count
#         try:
#             rating_count_text = (
#                 page.locator("span.infoRatingCount-lKBiTI").inner_text().strip()
#             )
#             result["rating_count"] = int(
#                 "".join(filter(str.isdigit, rating_count_text))
#             )
#         except Exception as e:
#             print("Gagal mengambil rating count:", e)

#         # Ambil jumlah terjual
#         try:
#             sold_text = page.locator("div.info__sold-ZdTfzQ").inner_text().strip()
#             sold_num_str = sold_text.lower().replace("sold", "").strip()

#             if "k" in sold_num_str:
#                 sold_value = float(sold_num_str.replace("k", "")) * 1000
#             elif "m" in sold_num_str:
#                 sold_value = float(sold_num_str.replace("m", "")) * 1_000_000
#             else:
#                 sold_value = float(sold_num_str)

#             result["sold"] = int(sold_value)
#         except Exception as e:
#             print("Gagal mengambil jumlah terjual:", e)

#         # Klik tombol "Select options"
#         try:
#             page.locator("text=Select options").click(force=True)
#             page.wait_for_selector(".skuMain-zLbDSB", timeout=7000)
#         except Exception as e:
#             print("Gagal klik tombol Select Options:", e)

#         # Variasi "Masa Aktif"
#         try:
#             masa_aktif_locator = page.locator(
#                 ".title-U0a3zD", has_text="Masa Aktif"
#             ).locator("xpath=../following-sibling::div[1]/div")
#             masa_aktif_count = masa_aktif_locator.count()
#         except Exception as e:
#             print("Gagal mendapatkan varians Masa Aktif:", e)
#             masa_aktif_count = 0

#         for i in range(masa_aktif_count):
#             masa_aktif_option = masa_aktif_locator.nth(i)
#             masa_aktif_text = masa_aktif_option.inner_text().strip()
#             masa_aktif_option.click()
#             page.wait_for_timeout(300)

#             # Variasi "Kuota"
#             try:
#                 kuota_locator = page.locator(".title-U0a3zD", has_text="Kuota").locator(
#                     "xpath=../following-sibling::div[1]/div"
#                 )
#                 kuota_count = kuota_locator.count()
#             except Exception as e:
#                 print("Gagal mendapatkan varians Kuota:", e)
#                 kuota_count = 0

#             for j in range(kuota_count):
#                 kuota_option = kuota_locator.nth(j)
#                 kuota_text = kuota_option.inner_text().strip()
#                 kuota_option.click()
#                 page.wait_for_timeout(400)

#                 try:
#                     price = page.locator(".price-LYdk0Q span").inner_text().strip()
#                 except Exception as e:
#                     print("Gagal mendapatkan harga:", e)
#                     price = "?"

#                 result["variants"].append(
#                     {"Masa Aktif": masa_aktif_text, "kuota": kuota_text, "price": price}
#                 )

#         # Simpan hasil ke file
#         with open("response.json", "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)

#         print("Success save to response.json")
#         browser.close()
#         return result


from playwright.sync_api import sync_playwright
import json


def scrape(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(6000)

        result = {
            "title": None,
            "sold": None,
            "rating": None,
            "rating_count": None,
            "variants": [],
        }

        # Ambil judul produk
        try:
            title_locator = page.locator(".title-v0v6fK")
            title_locator.wait_for(timeout=5000)
            result["title"] = title_locator.inner_text().strip()
        except Exception as e:
            print("Gagal mengambil judul produk:", e)

        # Ambil rating
        try:
            rating_text = (
                page.locator("span.infoRatingScore-jSs6kd").inner_text().strip()
            )
            result["rating"] = float(rating_text)
        except Exception as e:
            print("Gagal mengambil rating:", e)

        # Ambil rating count
        try:
            rating_count_text = (
                page.locator("span.infoRatingCount-lKBiTI").inner_text().strip()
            )
            result["rating_count"] = int(
                "".join(filter(str.isdigit, rating_count_text))
            )
        except Exception as e:
            print("Gagal mengambil rating count:", e)

        # Ambil jumlah terjual
        try:
            sold_text = page.locator("div.info__sold-ZdTfzQ").inner_text().strip()
            sold_num_str = sold_text.lower().replace("sold", "").strip()
            if "k" in sold_num_str:
                sold_value = float(sold_num_str.replace("k", "")) * 1000
            elif "m" in sold_num_str:
                sold_value = float(sold_num_str.replace("m", "")) * 1_000_000
            else:
                sold_value = float(sold_num_str)
            result["sold"] = int(sold_value)
        except Exception as e:
            print("Gagal mengambil jumlah terjual:", e)

        # Klik tombol "Select options"
        try:
            page.locator("text=Select options").click(force=True)
            page.wait_for_selector(".skuMain-zLbDSB", timeout=7000)
        except Exception as e:
            print("Gagal klik tombol Select Options:", e)

        # Cari dan klik kombinasi "Masa Aktif" dan "Kuota"
        try:
            masa_aktif_locator = page.locator(
                ".title-U0a3zD", has_text="Masa Aktif"
            ).locator("xpath=../following-sibling::div[1]/div")
            kuota_locator = page.locator(".title-U0a3zD", has_text="Kuota").locator(
                "xpath=../following-sibling::div[1]/div"
            )

            for i in range(masa_aktif_locator.count()):
                masa_aktif_option = masa_aktif_locator.nth(i)
                masa_aktif_text = masa_aktif_option.inner_text().strip()
                masa_aktif_option.click()
                page.wait_for_timeout(300)

                for j in range(kuota_locator.count()):
                    kuota_option = kuota_locator.nth(j)
                    kuota_text = kuota_option.inner_text().strip()
                    kuota_option.click()
                    page.wait_for_timeout(400)

                    try:
                        price = page.locator(".price-LYdk0Q span").inner_text().strip()
                    except Exception as e:
                        print("Gagal mendapatkan harga:", e)
                        price = "?"

                    result["variants"].append(
                        {
                            "Masa Aktif": masa_aktif_text,
                            "kuota": kuota_text,
                            "price": price,
                        }
                    )
        except Exception as e:
            print("Gagal mengambil kombinasi Masa Aktif dan Kuota:", e)

        # Tambahan: cek dan klik varian lain satu per satu
        extra_options = [
            "Ukuran/Size",
            "Spesifikasi",
            "Masa Aktif, FUP",
            "Paket",
            "Variant",
        ]
        for opt_name in extra_options:
            try:
                locator = page.locator(".title-U0a3zD", has_text=opt_name).locator(
                    "xpath=../following-sibling::div[1]/div"
                )
                for i in range(locator.count()):
                    opt = locator.nth(i)
                    opt_text = opt.inner_text().strip()
                    opt.click()
                    page.wait_for_timeout(400)
                    try:
                        price = page.locator(".price-LYdk0Q span").inner_text().strip()
                    except:
                        price = "?"
                    result["variants"].append({opt_name: opt_text, "price": price})
            except Exception as e:
                print(f"Gagal mendapatkan opsi tambahan {opt_name}: {e}")

        # Simpan hasil ke file
        with open("response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("Success save to response.json")
        browser.close()
        return result
