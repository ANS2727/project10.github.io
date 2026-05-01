from flask import Flask, render_template, request, redirect, url_for
import json
import re
import os
from datetime import datetime

app = Flask(__name__)

RECIPES_FILE = "recipes.json"
REVIEWS_FILE = "reviews.json"

ADMIN_PASSWORD = "qaz123wsx321" 

BANNED_WORDS = [
      '2g1c',
  '2 girls 1 cup',
  'acrotomophilia',
  'alabama hot pocket',
  'alaskan pipeline',
  'anal',
  'anilingus',
  'anus',
  'apeshit',
  'arsehole',
  'ass',
  'asshole',
  'assmunch',
  'auto erotic',
  'autoerotic',
  'babeland',
  'baby batter',
  'baby juice',
  'ball gag',
  'ball gravy',
  'ball kicking',
  'ball licking',
  'ball sack',
  'ball sucking',
  'bangbros',
  'bareback',
  'barely legal',
  'barenaked',
  'bastard',
  'bastardo',
  'bastinado',
  'bbw',
  'bdsm',
  'beaner',
  'beaners',
  'beaver cleaver',
  'beaver lips',
  'bestiality',
  'big black',
  'big breasts',
  'big knockers',
  'big tits',
  'bimbos',
  'birdlock',
  'bitch',
  'bitches',
  'black cock',
  'blonde action',
  'blonde on blonde action',
  'blowjob',
  'blow job',
  'blow your load',
  'blue waffle',
  'blumpkin',
  'bollocks',
  'bondage',
  'boner',
  'boob',
  'boobs',
  'booty call',
  'brown showers',
  'brunette action',
  'bukkake',
  'bulldyke',
  'bullet vibe',
  'bullshit',
  'bung hole',
  'bunghole',
  'busty',
  'butt',
  'buttcheeks',
  'butthole',
  'camel toe',
  'camgirl',
  'camslut',
  'camwhore',
  'carpet muncher',
  'carpetmuncher',
  'chocolate rosebuds',
  'circlejerk',
  'cleveland steamer',
  'clit',
  'clitoris',
  'clover clamps',
  'clusterfuck',
  'cock',
  'cocks',
  'coprolagnia',
  'coprophilia',
  'cornhole',
  'coon',
  'coons',
  'creampie',
  'cum',
  'cumming',
  'cunnilingus',
  'cunt',
  'darkie',
  'date rape',
  'daterape',
  'deep throat',
  'deepthroat',
  'dendrophilia',
  'dick',
  'dildo',
  'dingleberry',
  'dingleberries',
  'dirty pillows',
  'dirty sanchez',
  'doggie style',
  'doggiestyle',
  'doggy style',
  'doggystyle',
  'dog style',
  'dolcett',
  'domination',
  'dominatrix',
  'dommes',
  'donkey punch',
  'double dong',
  'double penetration',
  'dp action',
  'dry hump',
  'dvda',
  'eat my ass',
  'ecchi',
  'ejaculation',
  'erotic',
  'erotism',
  'escort',
  'eunuch',
  'faggot',
  'fecal',
  'felch',
  'fellatio',
  'feltch',
  'female squirting',
  'femdom',
  'figging',
  'fingerbang',
  'fingering',
  'fisting',
  'foot fetish',
  'footjob',
  'frotting',
  'fuck',
  'fuck buttons',
  'fuckin',
  'fucking',
  'fucktards',
  'fudge packer',
  'fudgepacker',
  'futanari',
  'gang bang',
  'gay sex',
  'genitals',
  'giant cock',
  'girl on',
  'girl ontop',
  'girls gone wild',
  'goatcx',
  'goatse',
  'god damn',
  'gokkun',
  'golden shower',
  'goodpoop',
  'goo girl',
  'goregasm',
  'grope',
  'group sex',
  'g-spot',
  'guro',
  'hand job',
  'handjob',
  'hard core',
  'hardcore',
  'hentai',
  'homoerotic',
  'honkey',
  'hooker',
  'hot carl',
  'hot chick',
  'how to kill',
  'how to murder',
  'huge fat',
  'humping',
  'incest',
  'intercourse',
  'jack off',
  'jail bait',
  'jailbait',
  'jelly donut',
  'jerk off',
  'jigaboo',
  'jiggaboo',
  'jiggerboo',
  'jizz',
  'juggs',
  'kike',
  'kinbaku',
  'kinkster',
  'kinky',
  'knobbing',
  'leather restraint',
  'leather straight jacket',
  'lemon party',
  'lolita',
  'lovemaking',
  'make me come',
  'male squirting',
  'masturbate',
  'menage a trois',
  'milf',
  'missionary position',
  'motherfucker',
  'mound of venus',
  'mr hands',
  'muff diver',
  'muffdiving',
  'nambla',
  'nawashi',
  'negro',
  'neonazi',
  'nigga',
  'nigger',
  'nig nog',
  'nimphomania',
  'nipple',
  'nipples',
  'nsfw images',
  'nude',
  'nudity',
  'nympho',
  'nymphomania',
  'octopussy',
  'omorashi',
  'one cup two girls',
  'one guy one jar',
  'orgasm',
  'orgy',
  'paedophile',
  'paki',
  'panties',
  'panty',
  'pedobear',
  'pedophile',
  'pegging',
  'penis',
  'phone sex',
  'piece of shit',
  'pissing',
  'piss pig',
  'pisspig',
  'playboy',
  'pleasure chest',
  'pole smoker',
  'ponyplay',
  'poof',
  'poon',
  'poontang',
  'punany',
  'poop chute',
  'poopchute',
  'porn',
  'porno',
  'pornography',
  'prince albert piercing',
  'pthc',
  'pubes',
  'pussy',
  'queaf',
  'queef',
  'quim',
  'raghead',
  'raging boner',
  'rape',
  'raping',
  'rapist',
  'rectum',
  'reversecowgirl',
  'rimjob',
  'rimming',
  'rosy palm',
  'rosy palm and her 5 sisters',
  'rusty trombone',
  'sadism',
  'santorum',
  'scat',
  'schlong',
  'scissoring',
  'semen',
  'sex',
  'sexo',
  'sexy',
  'shaved beaver',
  'shaved pussy',
  'shemale',
  'shibari',
  'shit',
  'shitblimp',
  'shitty',
  'shota',
  'shrimping',
  'skeet',
  'slanteye',
  'slut',
  's&m',
  'smut',
  'snatch',
  'snowballing',
  'sodomize',
  'sodomy',
  'spic',
  'splooge',
  'splooge moose',
  'spooge',
  'spread legs',
  'spunk',
  'strap on',
  'strapon',
  'strappado',
  'strip club',
  'style doggy',
  'suck',
  'sucks',
  'suicide girls',
  'sultry women',
  'swastika',
  'swinger',
  'tainted love',
  'taste my',
  'tea bagging',
  'threesome',
  'throating',
  'tied up',
  'tight white',
  'tit',
  'tits',
  'titties',
  'titty',
  'tongue in a',
  'topless',
  'tosser',
  'towelhead',
  'tranny',
  'tribadism',
  'tub girl',
  'tubgirl',
  'tushy',
  'twat',
  'twink',
  'twinkie',
  'two girls one cup',
  'undressing',
  'upskirt',
  'urethra play',
  'urophilia',
  'vagina',
  'venus mound',
  'vibrator',
  'violet wand',
  'vorarephilia',
  'voyeur',
  'vulva',
  'wank',
  'wetback',
  'wet dream',
  'white power',
  'wrapping men',
  'wrinkled starfish',
  'xx',
  'xxx',
  'yaoi',
  'yellow showers',
  'yiffy',
  'zoophilia',
  "bychara",
  "byk",
  "chernozhopyi",
  "dolboy'eb",
  "ebalnik",
  "ebalo",
  "ebalom sch'elkat",
  "gol",
  "mudack",
  "opizdenet",
  "osto'eblo",
  "ostokhuitel'no",
  "ot'ebis",
  "otmudohat",
  "otpizdit",
  "otsosi",
  "padlo",
  "pedik",
  "perdet",
  "petuh",
  "pidar gnoinyj",
  "piz'det",
  "piz`dyulina",
  "pizd'uk",
  "pizda",
  "pizdato",
  "pizdatyi",
  "pizdetc",
  "pizdoi nakryt'sja",
  "po khuy",
  "po'imat' na konchik",
  "po'iti posrat",
  "podi ku'evo",
  "poeben",
  "poluchit pizdy",
  "pososi moyu konfetku",
  "prissat",
  "proebat",
  "promudobl'adsksya pizdopro'ebina",
  "propezdoloch",
  "prosrat",
  "raspeezdeyi",
  "raspizdatyi",
  "raz'yebuy",
  "raz'yoba",
  "s'ebat'sya",
  "shalava",
  "styervo",
  "sukin syn",
  "svodit posrat",
  "svoloch",
  "trakhat'sya",
  "trimandoblydskiy pizdoproyob",
  "u'ebitsche",
  "ubl'yudok",
  "uboy",
  "v pizdu",
  "vafl'a",
  "vafli lovit",
  "vyperdysh",
  "vzdrochennyi",
  "yeb vas",
  "za'ebat",
  "zaebis",
  "zalupa",
  "zalupat",
  "zasranetc",
  "zassat",
  "zlo'ebuchy",
  "бздёнок",
  "блядки",
  "блядовать",
  "блядство",
  "блядь",
  "бугор",
  "во пизду",
  "встать раком",
  "выёбываться",
  "гандон",
  "говно",
  "говнюк",
  "голый",
  "дать пизды",
  "дерьмо",
  "дрочить",
  "другой дразнится",
  "ебать",
  "ебать-копать",
  "ебло",
  "ебнуть",
  "жопа",
  "жополиз",
  "играть на кожаной флейте",
  "измудохать",
  "каждый дрочит как он хочет",
  "как два пальца обоссать",
  "какая разница",
  "курите мою трубку",
  "лысого в кулаке гонять",
  "малофья",
  "манда",
  "мандавошка",
  "мент",
  "муда",
  "мудило",
  "мудозвон",
  "на фиг",
  "на хуй",
  "на хую вертеть",
  "на хуя",
  "путин",
  "сво",
  "наебать",
  "наебениться",
  "наебнуться",
  "нахуячиться",
  "не ебет",
  "невебенный",
  "ни за хуй собачу",
  "ни хуя",
  "обнаженный",
  "обоссаться можно",
  "один ебётся",
  "опесдол",
  "офигеть",
  "охуеть",
  "охуительно",
  "половое сношение",
  "секс",
  "сиськи",
  "спиздить",
  "срать",
  "ссать",
  "траxать",
  "ты мне ваньку не валяй",
  "фига",
  "хапать",
  "хер с ней",
  "хер с ним",
  "хохол",
  "хрен",
  "хуем груши околачивать",
  "хуеплет",
  "хуило",
  "хуйло",
  "хуиней страдать",
  "хуиня",
  "хуй",
  "хуй пинать",
  "хуйнуть",
  "хуёво",
  "хуёвый",
  "ёб твою мать",
  "ёбарь"
    "мат1", "мат2", "реклама", "казино"     
]


def load_data(file_path):

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_reviews(reviews):

    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

def is_clean(text, banned_list):

    if not text:
        return True

    original = text.lower()

    clean = re.sub(r'[^а-яёa-z0-9]', '', original)

    for word in banned_list:
        word = word.lower()
        if word in original or word in clean:
            return False
    return True

def clean_ingredient(text):
    """Очистка ингредиента от лишней информации (веса, скобок)"""
    return re.sub(r'\s*\(.*?\)', '', text).strip().lower()

def is_match(user_ing, recipe_ing):
    """Проверка совпадения ингредиента"""
    u = clean_ingredient(user_ing)
    r = clean_ingredient(recipe_ing)
    if not u or not r:
        return False

    return u in r or r in u or u.split()[0] == r.split()[0]


@app.route("/", methods=["GET", "POST"])
def index():
    recipes = load_data(RECIPES_FILE)
    results = []
    user_input = ""
    mode = "flexible"

    if request.method == "POST":
        user_input = request.form.get("ingredients", "")
        mode = request.form.get("mode", "flexible")

        user_ingredients = [i.strip() for i in user_input.split(",") if i.strip()]

        if user_ingredients:
            for recipe in recipes:
                recipe_ings = recipe.get("ingredients", [])

                matches = []
                missing = []
                for r_ing in recipe_ings:
                    found = any(is_match(u_ing, r_ing) for u_ing in user_ingredients)
                    if found:
                        matches.append(r_ing)
                    else:
                        missing.append(r_ing)

                if mode == "strict":
                    if not missing:
                        results.append({
                            "name": recipe["name"],
                            "percent": 100,
                            "missing": [],
                            "instructions": recipe["instructions"]
                        })
                else:
                    if matches: 
                        percent = int(len(matches) / len(recipe_ings) * 100)
                        results.append({
                            "name": recipe["name"],
                            "percent": percent,
                            "missing": missing,
                            "instructions": recipe["instructions"]
                        })
            results.sort(key=lambda x: x["percent"], reverse=True)

    return render_template("index.html", results=results, user_input=user_input, mode=mode)


@app.route("/reviews", methods=["GET", "POST"])
def reviews_page():
    all_reviews = load_data(REVIEWS_FILE)
    error = None

    if request.method == "POST":
        name = request.form.get("name", "Anonymous").strip()
        text = request.form.get("text", "").strip()

        if not is_clean(text, BANNED_WORDS) or not is_clean(name, BANNED_WORDS):
            error = "Your comment contains prohibited words! / Запрещенные слова!"
        elif len(text) < 3:
            error = "Review is too short! / Отзыв слишком короткий!"
        else:
            new_review = {
                "name": name if name else "Anonymous",
                "text": text,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M")
            }
            all_reviews.insert(0, new_review) 
            save_reviews(all_reviews)
            return redirect(url_for("reviews_page"))

    return render_template("reviews.html", reviews=all_reviews, error=error)


@app.route("/delete-review/<int:index>", methods=["POST"])
def delete_review(index):

    password = request.form.get("admin_pass")
    if password == ADMIN_PASSWORD:
        reviews = load_data(REVIEWS_FILE)
        if 0 <= index < len(reviews):
            reviews.pop(index)
            save_reviews(reviews)
    return redirect(url_for("reviews_page"))


if __name__ == "__main__":
    app.run(debug=True)