# utils/lang.py


def get_labels():
    return {
        "English": {
            "title": "Portfolio Builder",
            "capital_label": "Enter your total investment capital (R$):",
            "no_data": "No stocks found with margin of safety greater than 50%.",
            "toggle_label": "Allocation mode:",
            "toggle_options": ["Standard B3 lots (100 shares)", "Individual shares"],
            "info_lot": "Note: Share quantities are rounded down to the nearest lot of 100 shares, as per standard B3 trading rules.",
            "info_unit": "Note: Share quantities are rounded down to the nearest individual share.",
            "section_header": "Suggested Portfolio",
            "columns": {
                "ticker": "Ticker",
                "company_name": "Company",
                "market_price": "Market Price (R$)",
                "margin_of_safety": "Margin of Safety",
                "normalized_weight": "Portfolio Weight",
                "shares": "Shares to Buy",
                "total_cost": "Total Cost (R$)",
            },
            "capital_used": "**Total capital used:** R$ {:.2f}",
            "cash_remaining": "**Remaining cash:** R$ {:.2f}",
        },
        "Português (BR)": {
            "title": "Construtor de Portfólio",
            "capital_label": "Informe o capital total para investir (R$):",
            "no_data": "Nenhuma ação encontrada com margem de segurança superior a 50%.",
            "toggle_label": "Modo de alocação:",
            "toggle_options": ["Lotes padrão da B3 (100 ações)", "Ações individuais"],
            "info_lot": "Nota: A quantidade de ações é arredondada para baixo ao lote de 100 ações, conforme padrão da B3.",
            "info_unit": "Nota: A quantidade de ações é arredondada para baixo à unidade.",
            "section_header": "Portfólio Sugerido",
            "columns": {
                "ticker": "Ticker",
                "company_name": "Empresa",
                "market_price": "Preço de Mercado (R$)",
                "margin_of_safety": "Margem de Segurança",
                "normalized_weight": "Peso no Portfólio",
                "shares": "Ações a Comprar",
                "total_cost": "Custo Total (R$)",
            },
            "capital_used": "**Capital utilizado:** R$ {:.2f}",
            "cash_remaining": "**Saldo restante:** R$ {:.2f}",
        },
    }
