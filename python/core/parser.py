def parse_response(data=None, platform=None, filepath="response.json"):
    import json

    def normalize_keys(d):
        return {k.strip().title(): v for k, v in d.items()}

    try:
        if data is None:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

        rows = []
        sold = data.get("sold")
        rating = data.get("rating")
        rating_count = data.get("rating_count")

        if platform == "tokopedia":
            variants = data.get("variants", [])
            for v in variants:
                v_norm = normalize_keys(v)
                rows.append(
                    {
                        "Masa Aktif": v_norm.get("Masa Aktif", ""),
                        "Kuota": v_norm.get("Kuota", ""),
                        "Harga": v_norm.get("Price", ""),
                    }
                )

        elif platform == "shopee":
            item = data.get("data", {})
            models = item.get("models", [])
            for model in models:
                model = normalize_keys(model)
                name = model.get("Name", "N/A")
                price_int = model.get("Price", 0)
                price_fmt = f"Rp. {int(price_int / 100000):,}".replace(",", ".")
                rows.append({"Nama Paket": name, "Harga": price_fmt})

        elif platform == "gkomunika":
            variants = data.get("variants", [])
            for v in variants:
                v_norm = normalize_keys(v)
                public_title = v_norm.get("Public_Title", "N/A")
                price = v_norm.get("Price", 0)
                price_fmt = f"Rp. {int(price / 100):,}".replace(",", ".")
                rows.append(
                    {
                        "Masa Aktif - Kuota": public_title,
                        "Harga": price_fmt,
                    }
                )

        elif platform == "gkomunika_id":
            variants = data.get("variants", [])
            for v in variants:
                v_norm = normalize_keys(v)
                rows.append(
                    {
                        "Masa Aktif": v_norm.get("Masa Aktif", ""),
                        "FUP": v_norm.get("Fup", ""),
                        "Harga": v_norm.get("Price", ""),
                    }
                )

        elif platform == "tiktok":
            if "title" in data and "variants" in data:
                for v in data["variants"]:
                    v_norm = normalize_keys(v)
                    rows.append(
                        {
                            "Masa Aktif": v_norm.get("Masa Aktif", ""),
                            "Kuota": v_norm.get("Kuota", ""),
                            "Harga": v_norm.get("Price", "N/A"),
                        }
                    )
        else:
            print(f"Platform {platform} belum didukung.")

        return rows, sold, rating, rating_count

    except Exception as e:
        print(f"Error saat parsing: {e}")
        return [], None, None, None
