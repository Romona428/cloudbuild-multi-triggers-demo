from fastapi import FastAPI, HTTPException, Query
import string, secrets

app = FastAPI()

AMBIGUOUS = set("Il1O0")
SYMBOLS =  "!@#$%^&*()-_=+[]{};:,.?/\\|~"

@app.get("/generate-passwd", summary="密碼產生器",
        description="參數：length(密碼長度)、count(要產生幾組) 及是否使用小寫/大寫/數字/符號；若啟用即保證至少 1 個(符號至多1個)。")
def generate(length:int=Query(12, ge=4, le=128),
    count:int=Query(1,  ge=1,  le=50),
    use_lower:bool=True,
    use_upper:bool=True,
    use_digits:bool=True,
    use_symbols:bool=True,
    exclude_ambiguous:bool=True):

    # 建立各子集合，並排除易混淆字元
    base_sets = []
    if use_lower: base_sets.append(string.ascii_lowercase)
    if use_upper: base_sets.append(string.ascii_uppercase)
    if use_digits: base_sets.append(string.digits)
    
    sym_set = SYMBOLS if use_symbols else ""

    if not base_sets:
        raise HTTPException(400, detail="請至少啟用符號以外的一種字元類別")
    
    if exclude_ambiguous:
        base_sets = ["".join(ch for ch in s if ch not in AMBIGUOUS) for s in base_sets]

    if len(base_sets)+1 > length:
        raise HTTPException(400, detail="length 太短，長度需滿足每類至少 1 個字元")
    
    charset = "".join(base_sets) 

    def gen(n:int) -> str:
        # 各類至少 1 個
        picks = [secrets.choice(s) for s in base_sets]
        # 符號最多 1 個：
        if use_symbols:
            picks.append(secrets.choice(sym_set))
        # 其餘由不含符號的 charset 補滿
        picks += [secrets.choice(charset) for _ in range(n-len(picks))]
        # 洗牌(Fisher-Yates)
        for i in range(len(picks)-1, 0, -1):
            j = secrets.randbelow(i+1)
            picks[i], picks[j] = picks[j], picks[i]
        return "".join(picks)

    return {"password": [gen(length) for _ in range(count)]} 


