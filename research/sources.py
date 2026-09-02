"""Stage 4: real women prominent in roughly 1990-95. Fame is the only criterion.
Domains are used for balance during assembly; sources.txt is emitted flat."""

SOURCES = {
"music": """Whitney Houston|Mariah Carey|Celine Dion|Toni Braxton|Gloria Estefan|Bonnie Raitt
Sheryl Crow|Melissa Etheridge|Natalie Cole|Annie Lennox|Sinead OConnor|Tori Amos
Alanis Morissette|Queen Latifah|Wynonna Judd|Vanessa Williams|Janet Jackson|Paula Abdul
Amy Grant|Sarah McLachlan|PJ Harvey|Liz Phair|Kim Deal|Kim Gordon|Courtney Love
Dolores ORiordan|Shirley Manson|Gwen Stefani|Tracy Chapman|Suzanne Vega|Kate Bush
Chrissie Hynde|Debbie Gibson|Tiffany Darwish|Taylor Dayne|Martika Marrero|Jody Watley
Karyn White|Regina Belle|Anita Baker|Patti LaBelle|Chaka Khan|Aretha Franklin
Gladys Knight|Diana Ross|Tina Turner|Cyndi Lauper|Belinda Carlisle|Susanna Hoffs
Stevie Nicks|Pat Benatar|Joan Osborne|Jewel Kilcher|Paula Cole|Lisa Loeb|Juliana Hatfield
Kim Cattrall|Neneh Cherry|Des Ree|Terence Trent|Lisa Stansfield|Sophie Hawkins
Deborah Harry|Siouxsie Sioux|Kathleen Hanna|Kim Shattuck|Donita Sparks|Kat Bjelland
Tanya Donelly|Kristin Hersh|Louise Post|Nina Gordon|Justine Frischmann|Sonya Aurora
Emmylou Harris|Rosanne Cash|Lucinda Williams|Mary Black|Enya Brennan|Loreena McKennitt
Toni Halliday|Harriet Wheeler|Elizabeth Fraser|Beth Gibbons|Bjork Gudmundsdottir""",

"country": """Reba McEntire|Trisha Yearwood|Mary Chapin Carpenter|Shania Twain|Pam Tillis
Patty Loveless|Suzy Bogguss|Lorrie Morgan|Tanya Tucker|Faith Hill|Deana Carter
Martina McBride|Alison Krauss|Kathy Mattea|Dolly Parton|Tammy Wynette|Loretta Lynn
Naomi Judd|Barbara Mandrell|Crystal Gayle|Terri Clark|Joy Lynn White|Kelly Willis""",

"film_tv": """Jodie Foster|Emma Thompson|Holly Hunter|Susan Sarandon|Jessica Tandy|Kathy Bates
Michelle Pfeiffer|Sharon Stone|Julia Roberts|Winona Ryder|Demi Moore|Meg Ryan
Sandra Bullock|Geena Davis|Anjelica Huston|Marisa Tomei|Mercedes Ruehl|Whoopi Goldberg
Angela Bassett|Uma Thurman|Linda Hamilton|Sigourney Weaver|Helen Hunt|Candice Bergen
Kirstie Alley|Jane Seymour|Delta Burke|Fran Drescher|Tea Leoni|Lisa Kudrow
Courteney Cox|Jennifer Aniston|Christina Applegate|Alicia Silverstone|Claire Danes
Neve Campbell|Yasmine Bleeth|Pamela Anderson|Jennie Garth|Shannen Doherty|Tori Spelling
Gabrielle Carteris|Courtney ThorneSmith|Heather Locklear|Josie Bissett|Daphne Zuniga
Nicollette Sheridan|Kimberlin Brown|Deidre Hall|Kristian Alfonso|Alison Sweeney
Meryl Streep|Glenn Close|Jessica Lange|Sally Field|Kathleen Turner|Melanie Griffith
Andie MacDowell|Laura Dern|Mary McDonnell|Joan Cusack|Diane Keaton|Bette Midler
Goldie Hawn|Rene Russo|Bridget Fonda|Lara Flynn|Sherilyn Fenn|Madchen Amick
Peggy Lipton|Joan Chen|Ashley Judd|Salma Hayek|Rosie Perez|Jennifer Lopez
Halle Berry|Vivica Fox|Nia Long|Regina King|Jada Pinkett|Queen Sonja
Juliette Binoche|Isabelle Adjani|Emmanuelle Beart|Sophie Marceau|Irene Jacob
Judi Dench|Maggie Smith|Helena Bonham|Kristin Scott|Miranda Richardson|Tilda Swinton
Kate Winslet|Minnie Driver|Rachel Weisz|Samantha Morton|Emily Watson|Saffron Burrows""",

"sport": """Steffi Graf|Monica Seles|Gabriela Sabatini|Arantxa Sanchez|Jana Novotna
Conchita Martinez|Mary Pierce|Kimiko Date|Natasha Zvereva|Jennifer Capriati
Lindsay Davenport|Nancy Kerrigan|Tonya Harding|Oksana Baiul|Kristi Yamaguchi
Bonnie Blair|Katarina Witt|Surya Bonaly|Jackie Joyner|Gail Devers|Sheryl Swoopes
Mia Hamm|Kristine Lilly|Julie Foudy|Michelle Akers|Brandi Chastain|Carla Overbeck
Joy Fawcett|Briana Scurry|Hege Riise|Silvia Neid|Rebecca Lobo|Lisa Leslie
Dawn Staley|Charlotte Smith|Jennifer Azzi|Katrina McClain|Nikki McCray|Kara Wolters
Jennifer Rizzotti|Teresa Weatherspoon|Ruthie Bolton|Cynthia Cooper|Andrea Stinson
Manuela Maleeva|Helena Sukova|Zina Garrison|Lori McNeil|Amanda Coetzer|Anke Huber
Martina Navratilova|Chris Evert|Nathalie Tauziat|Julie Halard|Sabine Hack
Shannon Miller|Kim Zmeskal|Dominique Dawes|Kerri Strug|Svetlana Boginskaya
Tatiana Gutsu|Lilia Podkopayeva|Chen Lu|Midori Ito|Yuka Sato|Nicole Bobek
Janet Evans|Summer Sanders|Krisztina Egerszegi|Franziska Bindsteiger|Dara Torres
Merlene Ottey|Gwen Torrence|Sandra Farmer|Sonia OSullivan|Liz McColgan|Uta Pippig
Annika Sorenstam|Betsy King|Patty Sheehan|Dottie Pepper|Meg Mallon|Beth Daniel
Laura Davies|Juli Inkster|Kelly Robbins|Liselotte Neumann|Helen Alfredsson|Donna Andrews""",

"models": """Cindy Crawford|Naomi Campbell|Christy Turlington|Linda Evangelista|Claudia Schiffer
Kate Moss|Helena Christensen|Tyra Banks|Niki Taylor|Stephanie Seymour|Carla Bruni
Yasmeen Ghauri|Karen Mulder|Nadja Auermann|Eva Herzigova|Elle Macpherson
Paulina Porizkova|Amber Valletta|Shalom Harlow|Kristen McMenamy|Veronica Webb
Beverly Peele|Tatjana Patitz|Christie Brinkley|Iman Abdulmajid|Rachel Hunter
Emma Sjoberg|Vendela Kirsebom|Bridget Hall|Trish Goff|Nadege DuBospertus""",

"novelists": """Toni Morrison|Amy Tan|Donna Tartt|Terry McMillan|Jane Smiley|Annie Proulx
Alice Walker|Maya Angelou|Anne Rice|Danielle Steel|Jackie Collins|Mary Clark
Sue Grafton|Patricia Cornwell|Barbara Kingsolver|Louise Erdrich|Isabel Allende
Margaret Atwood|Doris Lessing|Nadine Gordimer|Naomi Wolf|Susan Faludi|Camille Paglia
Bell Hooks|Sandra Cisneros|Julia Alvarez|Jamaica Kincaid|Gloria Naylor|Bharati Mukherjee
Anita Brookner|Penelope Fitzgerald|Muriel Spark|Beryl Bainbridge|Pat Barker
Jeanette Winterson|Angela Carter|Hilary Mantel|Rose Tremain|Helen Fielding
Arundhati Roy|Kiran Desai|Anchee Min|Gish Jen|Fae Ng|Cristina Garcia""",

"politics_news": """Hillary Clinton|Janet Reno|Ruth Ginsburg|Madeleine Albright|Dianne Feinstein
Barbara Boxer|Carol Braun|Ann Richards|Benazir Bhutto|Margaret Thatcher
Gro Brundtland|Tansu Ciller|Kim Campbell|Aung Suu|Rigoberta Menchu|Mary Robinson
Diane Sawyer|Barbara Walters|Connie Chung|Katie Couric|Christiane Amanpour
Jane Pauley|Lesley Stahl|Maria Shriver|Cokie Roberts|Andrea Mitchell|Judy Woodruff
Nina Totenberg|Linda Ellerbee|Deborah Norville|Paula Zahn|Joan Lunden|Meredith Vieira
Elizabeth Dole|Geraldine Ferraro|Pat Schroeder|Nancy Pelosi|Kay Hutchison|Olympia Snowe""",

"tabloid_scandal": """Marcia Clark|Heidi Fleiss|Lorena Bobbitt|Anita Hill|Gennifer Flowers
Paula Jones|Faye Resnick|Zsa Gabor|Leona Helmsley|Imelda Marcos|Ivana Trump
Marla Maples|Roseanne Barr|Anna Smith|Jenny McCarthy|Carmen Electra|Traci Lords""",

"comedy_talk": """Ellen DeGeneres|Rosie ODonnell|Janeane Garofalo|Paula Poundstone|Brett Butler
Margaret Cho|Joan Rivers|Phyllis Diller|Elayne Boosler|Rita Rudner|Sandra Bernhard
Oprah Winfrey|Sally Raphael|Ricki Lake|Jenny Jones|Kathie Gifford|Julie Chen""",

"business_astro_royal": """Martha Stewart|Anita Roddick|Sherry Lansing|Dawn Steel|Linda Wachner
Sally Ride|Mae Jemison|Eileen Collins|Shannon Lucid|Kathryn Sullivan|Ellen Ochoa
Bonnie Dunbar|Tamara Jernigan|Nancy Currie|Susan Helms|Roberta Bondar|Helen Sharman
Chiaki Mukai|Yelena Kondakova|Diana Spencer|Sarah Ferguson|Queen Noor|Grace Kelly
Julia Child|Jane Goodall|Sylvia Earle|Temple Grandin|Mae West|Wendy Kopp""",
}

MONONYMS = ["Madonna", "Cher", "Bjork", "Sade", "Aaliyah", "Selena", "Enya",
            "Brandy", "Basia", "Roseanne", "Yanka", "Dido"]

def load():
    out = []
    for domain, blob in SOURCES.items():
        for entry in blob.replace('\n', '|').split('|'):
            e = entry.strip()
            if e and ' ' in e:
                first, last = e.rsplit(' ', 1)
                out.append((first.strip(), last.strip(), domain))
    return out

if __name__ == '__main__':
    rows = load()
    print(f"{len(rows)} named women across {len(SOURCES)} domains, plus {len(MONONYMS)} mononyms")
    from collections import Counter
    for d, n in Counter(r[2] for r in rows).most_common():
        print(f"  {d:<24} {n}")
