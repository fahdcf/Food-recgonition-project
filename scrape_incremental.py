from icrawler.builtin import BingImageCrawler, GoogleImageCrawler
import os
import random
import shutil
from pathlib import Path
import time
import logging
from PIL import Image
import hashlib

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# ----- Configuration -----
moroccan_dishes = {
    "couscous": [
        # English queries
        "traditional moroccan couscous family", "couscous fessi fez style", "couscous with turnips carrots",
        "maghrebi couscous plate", "steamed couscous semolina grains", "couscous berbere north africa",
        "festive couscous moroccan celebration", "homemade moroccan couscous bowl", "authentic couscous tagra recipe",
        "moroccan couscous meat stew", "couscous kabyle algerian moroccan", "couscous with pumpkin chickpeas",
        "traditional friday couscous morocco", "moroccan couscous seven vegetables", "couscous tfaya with raisins onions",
        "moroccan couscous lamb meat", "couscous royal morocco authentic", "berber couscous traditional dish",
        "moroccan couscous overhead view", "couscous marrakech style plate", "authentic moroccan couscous recipe",
        "couscous morocco street food", "homemade couscous semolina grains", "moroccan couscous clay pot",
        "couscous with chickpeas vegetables morocco", "traditional couscous north africa", "moroccan couscous family meal",
        "couscous fes traditional style", "moroccan couscous closeup food photography", "authentic couscous maghreb cuisine",
        "couscous morocco rustic presentation", "traditional moroccan couscous bowl", "couscous casablanca homestyle",
        "moroccan couscous with meat broth", "couscous tagine combination morocco", "authentic couscous berber recipe",
        "moroccan couscous festive occasion", "couscous seven vegetables morocco", "traditional friday couscous maghreb",
        # French queries
        "couscous marocain traditionnel fait maison", "couscous royal marocain légumes viande", "couscous fassi fès authentique",
        "couscous berbère maghreb cuisine", "couscous marocain tfaya oignons raisins", "couscous traditionnel nord africain",
        "couscous marocain sept légumes", "couscous casablancais style marocain", "couscous marocain agneau merguez",
        "couscous fait maison semoule grains", "couscous fête marocaine célébration", "couscous vendredi traditionnel maroc",
        "couscous marocain plat complet", "couscous authentique recette marocaine", "couscous marrakchi style marrakech",
        "couscous marocain viande légumes pois chiches", "couscous traditionnel tagine maroc", "couscous marocain sauce rouge",
        "couscous berbère montagne atlas", "couscous marocain présentation traditionnelle", "couscous royal fête marocaine",
        "couscous fassi recette authentique", "couscous marocain bol terre cuite", "couscous maghrébin plat familial",
        "couscous marocain cuisine de rue", "couscous traditionnel recette grand-mère", "couscous marocain légumes racines",
        "couscous royal maroc grande occasion", "couscous berbère authentique fait maison", "couscous marocain vapeur traditionnel",
        "couscous fassi légumes sept sortes", "couscous marocain repas convivial", "couscous traditionnel maghreb authentique",
        "couscous marocain plat national", "couscous royal légumes viande poulet", "couscous berbère cuisine traditionnelle",
        "couscous marocain closeup photographie culinaire", "couscous traditionnel présentation rustique", "couscous marocain recette originale",
        # Arabic queries  
        "كسكس مغربي تقليدي", "كسكس فاسي أصيل", "كسكس مغربي باللحم والخضر", 
        "كسكس بسبع خضر مغربي", "كسكس مغربي بالتفاية", "كسكس تقليدي مغربي",
        "كسكس مراكشي أصيل", "كسكس أمازيغي مغربي", "كسكس الجمعة المغربي",
        "كسكس مغربي باللحم", "كسكس بالدجاج مغربي", "كسكس فاسي باللحم",
        "كسكس مغربي منزلي", "كسكس تقليدي بالخضر", "كسكس مغربي بالحمص",
        "كسكس أمازيغي أصيل", "كسكس مغربي بالزيت", "كسكس فاسي تقليدي",
        "كسكس مغربي بالقرع", "كسكس بالخضر السبعة", "كسكس مغربي باللفت",
        "كسكس تقليدي فاسي", "كسكس مغربي عائلي", "كسكس أصيل بالمرق",
        "كسكس مغربي بالبصلة", "كسكس بالزبيب مغربي", "كسكس تقليدي منزلي",
        "كسكس مغربي طبق وطني", "كسكس فاسي باللحم والخضر", "كسكس أمازيغي جبلي",
        "كسكس مغربي بالكابوية", "كسكس تقليدي بالسمن", "كسكس مغربي أصيل",
        "كسكس بالدجاج البلدي", "كسكس مغربي طبق كامل", "كسكس فاسي عريق",
        "كسكس مغربي بالخليع", "كسكس تقليدي بالمصران", "كسكس أمازيغي تقليدي"
    ],
    "tagine": [
        # English queries
        "traditional earthenware tagine pot", "tagine djaj beldi free range chicken", "slow cooked tagine moroccan spices",
        "tagine with dates walnuts", "moroccan tagine clay pot cooking", "tagine bidaoui casablanca style",
        "tagine with green peas pearl onions", "berber tagine mountain recipe", "tagine mchermel tomato sauce",
        "moroccan tagine with chickpeas raisins", "tagine with sweet potatoes prunes", "authentic moroccan tagine home cooking",
        "tagine fassi fez traditional recipe", "moroccan lamb tagine apricots", "chicken tagine preserved lemons olives",
        "beef tagine moroccan vegetables", "tagine morocco clay pot dish", "traditional tagine north africa",
        "moroccan tagine with almonds honey", "tagine marrakech street food", "authentic tagine berber cuisine",
        "tagine djaj chicken moroccan style", "moroccan tagine slow cooked meat", "tagine with quinces cinnamon",
        "traditional moroccan tagine recipe", "tagine with artichokes peas", "moroccan tagine clay cooking pot",
        "tagine lamb prunes almonds morocco", "chicken tagine moroccan spices", "beef tagine with vegetables morocco",
        "tagine morocco traditional cooking", "moroccan tagine homemade authentic", "tagine with dried fruits nuts",
        "traditional tagine earthenware pot", "moroccan tagine festive dish", "tagine berber mountain style",
        "tagine morocco closeup food photography", "authentic tagine fez recipe", "moroccan tagine rustic presentation",
        # French queries
        "tajine marocain traditionnel authentique", "tajine poulet citrons confits olives", "tajine agneau pruneaux amandes",
        "tajine marocain plat terre cuite", "tajine fassi fès traditionnel", "tajine berbère cuisine marocaine",
        "tajine marocain légumes viande", "tajine poulet beldi fermier", "tajine bœuf légumes marocain",
        "tajine marocain coings cannelle", "tajine djaj poulet marocain", "tajine traditionnel cuisson lente",
        "tajine marocain fait maison", "tajine marrakchi style marrakech", "tajine marocain épices ras el hanout",
        "tajine agneau abricots marocain", "tajine poulet marocain tomates", "tajine berbère montagne atlas",
        "tajine marocain présentation traditionnelle", "tajine fassi recette originale", "tajine marocain plat convivial",
        "tajine poulet pommes de terre", "tajine marocain artichauts petits pois", "tajine agneau légumes racines",
        "tajine traditionnel maghreb authentique", "tajine marocain miel amandes", "tajine casablancais style bidaoui",
        "tajine marocain pois chiches raisins secs", "tajine poulet sauce rouge", "tajine berbère authentique fait maison",
        "tajine marocain patates douces", "tajine fassi cuisine traditionnelle", "tajine marocain fête célébration",
        "tajine agneau oignons caramélisés", "tajine poulet citrons confits", "tajine marocain closeup photographie",
        "tajine traditionnel plat national", "tajine marocain cuisson vapeur", "tajine berbère recette ancestrale",
        # Arabic queries
        "طاجين مغربي تقليدي", "طاجين بالدجاج البلدي", "طاجين باللحم والخضر",
        "طاجين فاسي أصيل", "طاجين مغربي بالبرقوق", "طاجين الدجاج بالزيتون",
        "طاجين مراكشي تقليدي", "طاجين أمازيغي مغربي", "طاجين باللحم والبصل",
        "طاجين مغربي بالحامض", "طاجين الدجاج المغربي", "طاجين تقليدي بالخضر",
        "طاجين فاسي باللحم", "طاجين مغربي بالسفرجل", "طاجين بالدجاج والليمون",
        "طاجين أمازيغي أصيل", "طاجين مغربي بالجزر", "طاجين باللوز والعسل",
        "طاجين تقليدي مغربي", "طاجين بالحمص مغربي", "طاجين باللحم والفواكه",
        "طاجين فاسي تقليدي", "طاجين مغربي بالبطاطس", "طاجين الدجاج الحامض",
        "طاجين أمازيغي جبلي", "طاجين مغربي بالزبيب", "طاجين باللحم المغربي",
        "طاجين تقليدي فاسي", "طاجين مغربي بالقوق", "طاجين بالدجاج البلدي",
        "طاجين مغربي أصيل", "طاجين باللحم والخوخ", "طاجين فاسي عريق",
        "طاجين أمازيغي تقليدي", "طاجين مغربي بالخضر", "طاجين الدجاج الفاسي",
        "طاجين مغربي منزلي", "طاجين باللحم البلدي", "طاجين تقليدي أصيل"
    ],
    "pastilla": [
        # English queries
        "moroccan pastilla powdered sugar cinnamon", "bastilla marrakchia traditional morocco", "pastilla au poulet amandes effilées",
        "moroccan pastilla phyllo dough layers", "pastilla marocaine authentique", "traditional pastilla wedding morocco",
        "moroccan b'stilla pigeon almonds", "pastilla warqa dough morocco", "sweet savory pastilla moroccan cuisine",
        "pastilla tetouanaise northern morocco", "authentic moroccan pastilla recipe homemade", "pastilla royale morocco celebration",
        "moroccan pastilla round golden crispy", "pastilla fassia fez traditional", "moroccan chicken pastilla almonds",
        "pastilla morocco phyllo layers sugar", "traditional bastilla pigeon meat", "moroccan pastilla wedding feast",
        "pastilla with almonds cinnamon morocco", "authentic pastilla fez recipe", "moroccan pastilla crispy golden",
        "pastilla royale traditional morocco", "chicken pastilla moroccan spices", "pastilla morocco festive dish",
        "traditional moroccan pastilla homemade", "pastilla with orange blossom water", "moroccan pastilla closeup layers",
        "pastilla fassi authentic fez", "bastilla morocco traditional recipe", "moroccan pastilla powdered sugar dusted",
        "pastilla with chicken eggs morocco", "traditional pastilla north africa", "moroccan pastilla rustic presentation",
        "pastilla morocco celebration dish", "authentic bastilla pigeon recipe", "moroccan pastilla phyllo crispy",
        "pastilla with saffron almonds", "traditional moroccan pastilla wedding", "pastilla morocco food photography",
        # French queries
        "pastilla marocaine traditionnelle authentique", "bastilla poulet amandes marocaine", "pastilla royale fête marocaine",
        "pastilla fassia fès recette originale", "pastilla marocaine feuilles brick", "pastilla traditionnelle pigeon amandes",
        "pastilla marocaine sucre glace cannelle", "bastilla marrakchia style marrakech", "pastilla marocaine feuilletée croustillante",
        "pastilla fassi cuisine traditionnelle", "pastilla marocaine mariage célébration", "pastilla poulet œufs amandes",
        "bastilla marocaine authentique fait maison", "pastilla traditionnelle recette ancestrale", "pastilla marocaine présentation élégante",
        "pastilla royale grande occasion", "pastilla fassia fès authentique", "pastilla marocaine warqa pâte feuilletée",
        "bastilla poulet épices marocaines", "pastilla marocaine sucré salé", "pastilla traditionnelle nord africain",
        "pastilla fassi recette traditionnelle", "pastilla marocaine dorée croustillante", "bastilla royale marocaine festive",
        "pastilla marocaine amandes effilées", "pastilla poulet cannelle sucre", "pastilla traditionnelle mariage marocain",
        "bastilla fassia cuisine marocaine", "pastilla marocaine closeup photographie", "pastilla royale présentation soignée",
        "pastilla marocaine eau fleur oranger", "bastilla traditionnelle pigeon sauvage", "pastilla fassi plat festif",
        "pastilla marocaine feuilletage doré", "bastilla poulet fait maison", "pastilla traditionnelle recette grand-mère",
        "pastilla marocaine safran amandes", "bastilla royale fête traditionnelle", "pastilla fassia authentique marocaine",
        # Arabic queries
        "بسطيلة مغربية تقليدية", "بسطيلة بالدجاج واللوز", "بسطيلة فاسية أصيلة",
        "بسطيلة مراكشية تقليدية", "بسطيلة مغربية بالورقة", "بسطيلة بالحمام المغربية",
        "بسطيلة فاسية باللوز", "بسطيلة مغربية بالسكر", "بسطيلة تقليدية مغربية",
        "بسطيلة بالدجاج البلدي", "بسطيلة فاسية عريقة", "بسطيلة مغربية بالقرفة",
        "بسطيلة أصيلة فاسية", "بسطيلة مراكشية باللوز", "بسطيلة مغربية منزلية",
        "بسطيلة تقليدية بالدجاج", "بسطيلة فاسية تقليدية", "بسطيلة مغربية بالبيض",
        "بسطيلة بالحمام الفاسية", "بسطيلة مغربية للأعراس", "بسطيلة تقليدية أصيلة",
        "بسطيلة فاسية بالورقة", "بسطيلة مغربية بالسكر الحلو", "بسطيلة بالدجاج المغربية",
        "بسطيلة أصيلة مغربية", "بسطيلة فاسية باللحم", "بسطيلة مراكشية عريقة",
        "بسطيلة تقليدية فاسية", "بسطيلة مغربية بماء الزهر", "بسطيلة بالدجاج واللوز",
        "بسطيلة فاسية للأفراح", "بسطيلة مغربية محمصة", "بسطيلة تقليدية بالحمام",
        "بسطيلة أصيلة بالدجاج", "بسطيلة فاسية منزلية", "بسطيلة مغربية بالزعفران",
        "بسطيلة مراكشية أصيلة", "بسطيلة تقليدية باللوز", "بسطيلة مغربية عريقة"
    ],
    "harira": [
        # English queries
        "harira soup moroccan bowl close up", "soupe harira marocaine ramadan iftar", "harira traditionnelle marocaine bol rouge",
        "moroccan harira garnished cilantro lemon", "harira soup spoon drizzle olive oil", "authentic harira morocco clay bowl",
        "harira soup overhead view ingredients", "traditional harira casablanca rbati style", "harira with bread chebakia dates",
        "moroccan harira winter soup steaming", "harira fassia traditional fez recipe", "harira soup rustic presentation morocco",
        "homemade harira thick red soup bowl", "moroccan harira ramadan soup traditional", "harira with lentils chickpeas morocco",
        "traditional harira soup north africa", "moroccan harira tomato based soup", "harira fassi fez authentic",
        "harira soup moroccan spices herbs", "traditional harira clay bowl presentation", "moroccan harira homemade recipe",
        "harira with vermicelli noodles morocco", "ramadan harira soup traditional", "moroccan harira thick hearty soup",
        "harira fassia traditional fez", "authentic harira moroccan cuisine", "harira soup steaming hot bowl",
        "traditional moroccan harira recipe", "harira with meat lentils morocco", "moroccan harira rustic clay bowl",
        "harira soup garnished fresh herbs", "traditional harira ramadan iftar", "moroccan harira closeup food photography",
        "harira with chickpeas tomatoes", "authentic harira fez recipe", "moroccan harira traditional presentation",
        # French queries
        "soupe harira marocaine traditionnelle", "harira ramadan marocaine iftar", "harira fassia fès authentique",
        "soupe harira marocaine lentilles pois chiches", "harira traditionnelle recette marocaine", "harira marocaine bol terre cuite",
        "soupe harira fassi cuisine traditionnelle", "harira marocaine épaisse rouge", "harira ramadan soupe traditionnelle",
        "soupe harira marocaine vermicelles", "harira fassia recette authentique", "harira marocaine persil coriandre citron",
        "soupe harira traditionnelle fait maison", "harira marocaine tomates lentilles", "harira fassi fès recette originale",
        "soupe harira ramadan marocaine fumante", "harira marocaine présentation rustique", "harira traditionnelle maghreb authentique",
        "soupe harira fassia épices marocaines", "harira marocaine bol rouge traditionnel", "harira ramadan recette ancestrale",
        "soupe harira marocaine viande légumes", "harira fassi cuisine marocaine", "harira traditionnelle closeup photographie",
        "soupe harira marocaine pois chiches", "harira ramadan soupe épaisse", "harira fassia plat traditionnel",
        "soupe harira marocaine présentation soignée", "harira traditionnelle bol fumant", "harira marocaine recette grand-mère",
        "soupe harira fassi lentilles viande", "harira ramadan marocaine authentique", "harira marocaine garniture fraîche",
        "soupe harira traditionnelle pain dattes", "harira fassia fès traditionnelle", "harira marocaine hiver réconfortante",
        # Arabic queries
        "حريرة مغربية تقليدية", "حريرة رمضانية مغربية", "حريرة فاسية أصيلة",
        "شوربة حريرة مغربية", "حريرة مغربية بالعدس", "حريرة تقليدية مغربية",
        "حريرة فاسية عريقة", "حريرة مغربية بالحمص", "حريرة رمضان المغربية",
        "حريرة فاسية تقليدية", "حريرة مغربية باللحم", "شوربة حريرة أصيلة",
        "حريرة تقليدية فاسية", "حريرة مغربية بالشعرية", "حريرة رمضانية فاسية",
        "حريرة فاسية باللحم", "حريرة مغربية حمراء", "شوربة حريرة تقليدية",
        "حريرة مغربية للإفطار", "حريرة فاسية بالعدس", "حريرة تقليدية بالحمص",
        "حريرة رمضان الفاسية", "حريرة مغربية كثيفة", "شوربة حريرة فاسية",
        "حريرة مغربية منزلية", "حريرة تقليدية باللحم", "حريرة فاسية أصيلة",
        "حريرة رمضانية تقليدية", "حريرة مغربية بالطماطم", "شوربة حريرة منزلية",
        "حريرة فاسية عتيقة", "حريرة مغربية بالمعكرونة", "حريرة تقليدية رمضان",
        "حريرة مغربية ساخنة", "حريرة فاسية بالحمص", "شوربة حريرة عريقة",
        "حريرة رمضانية أصيلة", "حريرة مغربية بالكرفس", "حريرة فاسية تقليدية"
    ],
    "rfissa": [
        # English queries
        "rfissa morocco plate shredded bread chicken", "moroccan rfissa msemmen layers authentic", "rfissa marocaine traditionnelle plat complet",
        "traditional rfissa trid chicken onion sauce", "moroccan rfissa fenugreek seeds helba", "rfissa plate overhead view morocco",
        "authentic rfissa casablanca homemade dish", "rfissa morocco celebration special occasion", "moroccan rfissa lentils chicken shredded bread",
        "rfissa traditional morocco clay plate", "rfissa with ras el hanout spices morocco", "moroccan rfissa postpartum new mother dish",
        "rfissa close up shredded msemmen chicken pieces", "traditional rfissa fez fassi recipe", "moroccan rfissa layered bread chicken",
        "rfissa morocco traditional berber dish", "authentic rfissa homemade moroccan", "rfissa with chicken onions morocco",
        "traditional rfissa morocco festive", "moroccan rfissa shredded flatbread layers", "rfissa fassi fez authentic recipe",
        "rfissa morocco clay serving dish", "traditional rfissa berber cuisine", "moroccan rfissa fenugreek chicken",
        "rfissa with msemmen bread morocco", "authentic rfissa traditional presentation", "moroccan rfissa celebratory dish",
        "rfissa morocco closeup food photography", "traditional rfissa casablanca style", "moroccan rfissa rustic serving",
        "rfissa with trid bread chicken sauce", "authentic rfissa fez recipe", "moroccan rfissa traditional layered dish",
        # French queries
        "rfissa marocaine traditionnelle authentique", "rfissa poulet msemmen déchiqueté", "rfissa fassia fès recette originale",
        "rfissa marocaine plat complet traditionnel", "rfissa berbère cuisine marocaine", "rfissa traditionnelle sauce oignons poulet",
        "rfissa marocaine fenugrec helba", "rfissa fassi fès authentique", "rfissa marocaine pain déchiré couches",
        "rfissa traditionnelle accouchement marocaine", "rfissa marocaine plat festif", "rfissa fassia recette ancestrale",
        "rfissa marocaine msemmen trid", "rfissa traditionnelle présentation rustique", "rfissa marocaine poulet beldi",
        "rfissa fassi cuisine traditionnelle", "rfissa marocaine sauce rouge oignons", "rfissa traditionnelle plat terre cuite",
        "rfissa marocaine célébration fête", "rfissa fassia plat complet", "rfissa traditionnelle closeup photographie",
        "rfissa marocaine pain feuilleté", "rfissa berbère recette authentique", "rfissa fassi fès traditionnelle",
        "rfissa marocaine épices ras el hanout", "rfissa traditionnelle casablanca bidaoui", "rfissa marocaine lentilles poulet",
        "rfissa fassia présentation soignée", "rfissa marocaine fait maison", "rfissa traditionnelle recette grand-mère",
        "rfissa marocaine sauce fenugrec", "rfissa fassi plat festif", "rfissa berbère cuisine traditionnelle",
        "rfissa marocaine msemmen déchiré", "rfissa traditionnelle authentique marocaine", "rfissa fassia fès recette originale",
        # Arabic queries
        "رفيسة مغربية تقليدية", "رفيسة فاسية أصيلة", "رفيسة مغربية بالدجاج",
        "رفيسة تقليدية بالمسمن", "رفيسة فاسية بالحلبة", "رفيسة مغربية بالترید",
        "رفيسة أصيلة مغربية", "رفيسة فاسية عريقة", "رفيسة مغربية بالبصل",
        "رفيسة تقليدية فاسية", "رفيسة مغربية بالعدس", "رفيسة بالدجاج البلدي",
        "رفيسة فاسية تقليدية", "رفيسة مغربية للنفاس", "رفيسة أصيلة بالمسمن",
        "رفيسة تقليدية مغربية", "رفيسة فاسية باللحم", "رفيسة مغربية منزلية",
        "رفيسة بالدجاج المغربية", "رفيسة فاسية بالبصل", "رفيسة تقليدية أصيلة",
        "رفيسة مغربية بالحلبة", "رفيسة فاسية للأفراح", "رفيسة أمازيغية مغربية",
        "رفيسة تقليدية بالدجاج", "رفيسة مغربية عريقة", "رفيسة فاسية منزلية",
        "رفيسة بالمسمن المغربية", "رفيسة تقليدية فاسية", "رفيسة مغربية بالتوابل",
        "رفيسة فاسية أصيلة", "رفيسة أمازيغية تقليدية", "رفيسة مغربية للولادة",
        "رفيسة تقليدية بالترید", "رفيسة فاسية بالحمص", "رفيسة مغربية طبق كامل"
    ],
    "mechoui": [
        # English queries
        "moroccan mechoui roasted whole lamb", "mechoui traditional berber morocco", "slow roasted mechoui lamb morocco",
        "mechoui morocco festive celebration", "traditional mechoui whole sheep roasted", "moroccan mechoui outdoor cooking",
        "mechoui berber atlas mountains", "authentic mechoui morocco recipe", "mechoui lamb roasted moroccan spices",
        "traditional mechoui wedding feast morocco", "moroccan mechoui crispy golden skin", "mechoui whole lamb slow roasted",
        "berber mechoui traditional cooking", "moroccan mechoui special occasion", "mechoui morocco rustic presentation",
        "traditional mechoui lamb cumin salt", "moroccan mechoui festive dish", "mechoui berber cuisine authentic",
        "slow cooked mechoui morocco", "traditional mechoui closeup lamb", "moroccan mechoui outdoor feast",
        "mechoui whole roasted sheep morocco", "berber mechoui atlas traditional", "moroccan mechoui celebration dish",
        "traditional mechoui moroccan spices", "mechoui lamb golden crispy", "moroccan mechoui rustic serving",
        "mechoui berber wedding feast", "traditional mechoui morocco authentic", "moroccan mechoui food photography",
        # French queries
        "méchoui marocain traditionnel agneau", "méchoui berbère atlas marocain", "méchoui agneau rôti entier maroc",
        "méchoui marocain fête traditionnelle", "méchoui berbère cuisine marocaine", "méchoui agneau cumin sel",
        "méchoui marocain cuisson lente", "méchoui traditionnel mariage berbère", "méchoui agneau doré croustillant",
        "méchoui marocain plein air", "méchoui berbère recette authentique", "méchoui agneau épices marocaines",
        "méchoui traditionnel célébration maroc", "méchoui marocain présentation rustique", "méchoui berbère montagne atlas",
        "méchoui agneau rôti traditionnel", "méchoui marocain grande occasion", "méchoui berbère plat festif",
        "méchoui traditionnel mouton entier", "méchoui marocain cuisine extérieure", "méchoui agneau marocain authentique",
        "méchoui berbère fête traditionnelle", "méchoui marocain closeup photographie", "méchoui traditionnel berbère marocain",
        "méchoui agneau cuisson traditionnelle", "méchoui marocain peau croustillante", "méchoui berbère recette ancestrale",
        "méchoui traditionnel plat convivial", "méchoui marocain agneau doré", "méchoui berbère cuisine traditionnelle",
        # Arabic queries
        "مشوي مغربي تقليدي", "مشوي أمازيغي بربري", "مشوي خروف كامل مغربي",
        "مشوي مغربي بالكمون", "مشوي تقليدي أمازيغي", "مشوي خروف مغربي",
        "مشوي بربري جبلي", "مشوي مغربي للأعراس", "مشوي تقليدي مغربي",
        "مشوي أمازيغي أصيل", "مشوي خروف بالملح", "مشوي مغربي محمص",
        "مشوي تقليدي بربري", "مشوي مغربي بالتوابل", "مشوي أمازيغي عريق",
        "مشوي خروف كامل", "مشوي مغربي للأفراح", "مشوي بربري تقليدي",
        "مشوي تقليدي أصيل", "مشوي مغربي ذهبي", "مشوي أمازيغي مغربي",
        "مشوي خروف مشوي", "مشوي مغربي احتفالي", "مشوي بربري أصيل",
        "مشوي تقليدي للولائم", "مشوي مغربي بطيء", "مشوي أمازيغي تقليدي",
        "مشوي خروف بالفرن", "مشوي مغربي عريق", "مشوي بربري منزلي"
    ],
    "zaalouk": [
        # English queries
        "zaalouk moroccan eggplant salad", "traditional zaalouk tomato eggplant", "zaalouk morocco cold appetizer",
        "moroccan zaalouk aubergine dish", "authentic zaalouk moroccan recipe", "zaalouk eggplant tomato morocco",
        "traditional zaalouk moroccan salad", "zaalouk morocco rustic presentation", "moroccan zaalouk olive oil garlic",
        "zaalouk eggplant dip morocco", "traditional zaalouk cold salad", "moroccan zaalouk closeup bowl",
        "zaalouk aubergine moroccan spices", "authentic zaalouk traditional morocco", "zaalouk eggplant salad moroccan",
        "traditional zaalouk appetizer morocco", "moroccan zaalouk tomato based", "zaalouk morocco homemade dish",
        "zaalouk eggplant moroccan cuisine", "traditional zaalouk rustic bowl", "moroccan zaalouk cold starter",
        "zaalouk aubergine traditional recipe", "authentic zaalouk morocco presentation", "zaalouk eggplant salad authentic",
        "traditional zaalouk moroccan cooking", "moroccan zaalouk food photography", "zaalouk eggplant dip traditional",
        # French queries
        "zaalouk marocain salade aubergines", "zaalouk traditionnel aubergines tomates", "zaalouk marocain entrée froide",
        "zaalouk aubergines épices marocaines", "zaalouk marocain recette authentique", "zaalouk traditionnel huile olive ail",
        "zaalouk marocain présentation rustique", "zaalouk aubergines tomates cuites", "zaalouk traditionnel salade marocaine",
        "zaalouk marocain caviar aubergines", "zaalouk aubergines recette traditionnelle", "zaalouk marocain bol terre cuite",
        "zaalouk traditionnel cuisine marocaine", "zaalouk marocain fait maison", "zaalouk aubergines plat froid",
        "zaalouk traditionnel closeup photographie", "zaalouk marocain entrée traditionnelle", "zaalouk aubergines authentique maroc",
        "zaalouk marocain présentation soignée", "zaalouk traditionnel recette ancestrale", "zaalouk aubergines épices cumin",
        "zaalouk marocain salade froide", "zaalouk traditionnel plat marocain", "zaalouk aubergines tomates ail",
        "zaalouk marocain authentique traditionnel", "zaalouk aubergines recette grand-mère", "zaalouk traditionnel cuisine marocaine",
        # Arabic queries
        "زعلوك مغربي تقليدي", "زعلوك بالباذنجان المغربي", "زعلوك مغربي بالطماطم",
        "زعلوك تقليدي مغربي", "سلطة زعلوك مغربية", "زعلوك بالباذنجان أصيل",
        "زعلوك مغربي بارد", "زعلوك تقليدي بالثوم", "زعلوك باذنجان مغربي",
        "زعلوك مغربي منزلي", "زعلوك تقليدي أصيل", "سلطة زعلوك تقليدية",
        "زعلوك بالباذنجان والطماطم", "زعلوك مغربي بالكمون", "زعلوك تقليدي مغربي",
        "زعلوك باذنجان بالثوم", "زعلوك مغربي عريق", "سلطة زعلوك باردة",
        "زعلوك تقليدي بالزيت", "زعلوك مغربي أصيل", "زعلوك بالباذنجان تقليدي",
        "زعلوك مغربي بالتوابل", "سلطة زعلوك منزلية", "زعلوك تقليدي بالطماطم",
        "زعلوك باذنجان عريق", "زعلوك مغربي طبق بارد", "زعلوك تقليدي أصيل"
    ],
    "msemmen": [
        # English queries
        "msemmen moroccan flatbread square", "traditional msemmen layered bread", "msemmen morocco breakfast bread",
        "moroccan msemmen folded flatbread", "authentic msemmen traditional recipe", "msemmen square layered morocco",
        "traditional msemmen moroccan pancake", "msemmen morocco golden crispy", "moroccan msemmen homemade bread",
        "msemmen folded square bread morocco", "traditional msemmen breakfast dish", "moroccan msemmen closeup layers",
        "msemmen layered flatbread authentic", "authentic msemmen morocco cooking", "msemmen square bread moroccan",
        "traditional msemmen crispy golden", "moroccan msemmen rustic presentation", "msemmen folded bread traditional",
        "msemmen morocco homemade recipe", "traditional msemmen layered pancake", "moroccan msemmen food photography",
        "msemmen square flatbread morocco", "authentic msemmen traditional bread", "msemmen moroccan breakfast staple",
        # French queries
        "msemmen marocain pain feuilleté", "msemmen traditionnel carré plié", "msemmen marocain petit-déjeuner",
        "msemmen pain feuilleté marocain", "msemmen traditionnel recette authentique", "msemmen marocain fait maison",
        "msemmen carré plié couches", "msemmen traditionnel doré croustillant", "msemmen marocain présentation rustique",
        "msemmen pain marocain traditionnel", "msemmen feuilleté carré marocain", "msemmen traditionnel cuisine marocaine",
        "msemmen marocain closeup photographie", "msemmen pain plié couches", "msemmen traditionnel recette ancestrale",
        "msemmen marocain galette feuilletée", "msemmen carré traditionnel maroc", "msemmen pain marocain authentique",
        "msemmen traditionnel petit-déjeuner marocain", "msemmen marocain recette grand-mère", "msemmen feuilleté doré croustillant",
        "msemmen traditionnel pain carré", "msemmen marocain cuisine traditionnelle", "msemmen pain plié marocain",
        # Arabic queries
        "مسمن مغربي تقليدي", "مسمن مربع مطوي", "مسمن مغربي للفطور",
        "مسمن تقليدي مغربي", "رغايف مسمن مغربي", "مسمن مغربي منزلي",
        "مسمن تقليدي مطوي", "مسمن مغربي مقرمش", "مسمن مربع مغربي",
        "مسمن تقليدي أصيل", "رغايف مسمن تقليدية", "مسمن مغربي ذهبي",
        "مسمن تقليدي بالسمن", "مسمن مغربي طبقات", "مسمن مربع تقليدي",
        "مسمن مغربي عريق", "رغايف مسمن منزلية", "مسمن تقليدي مغربي",
        "مسمن مغربي بالزيت", "مسمن مربع أصيل", "مسمن تقليدي للفطور",
        "مسمن مغربي محمص", "رغايف تقليدية مغربية", "مسمن مربع منزلي"
    ],
    "kefta_tagine": [
        # English queries
        "kefta tagine moroccan meatballs", "traditional kefta tagine eggs", "kefta tagine morocco tomato sauce",
        "moroccan kefta meatballs tagine pot", "authentic kefta tagine recipe", "kefta tagine with eggs morocco",
        "traditional kefta tagine moroccan spices", "kefta tagine morocco clay pot", "moroccan kefta tagine homemade",
        "kefta meatballs tagine traditional", "kefta tagine eggs tomato morocco", "traditional kefta tagine authentic",
        "moroccan kefta tagine closeup", "kefta tagine morocco rustic presentation", "kefta meatballs eggs tagine",
        "traditional kefta tagine moroccan dish", "moroccan kefta tagine food photography", "kefta tagine with tomatoes eggs",
        "kefta tagine morocco traditional cooking", "authentic kefta meatballs tagine", "kefta tagine moroccan cuisine",
        # French queries
        "tajine kefta marocain boulettes", "tajine kefta œufs traditionnel", "kefta tajine sauce tomate marocain",
        "tajine kefta marocain authentique", "kefta tajine boulettes œufs", "tajine kefta traditionnel recette",
        "kefta tajine marocain fait maison", "tajine kefta plat terre cuite", "kefta tajine œufs tomates maroc",
        "tajine kefta marocain épices", "kefta tajine traditionnel authentique", "tajine kefta boulettes viande",
        "kefta tajine marocain closeup", "tajine kefta présentation rustique", "kefta tajine recette traditionnelle",
        "tajine kefta marocain cuisine", "kefta tajine œufs sauce rouge", "tajine kefta traditionnel marocain",
        "kefta tajine photographie culinaire", "tajine kefta marocain recette ancestrale", "kefta tajine boulettes œufs",
        # Arabic queries
        "طاجين كفتة مغربي", "طاجين كفتة بالبيض", "كفتة مغربية بالطماطم",
        "طاجين كفتة تقليدي", "كفتة مغربية بالبيض", "طاجين كفتة أصيل",
        "كفتة تقليدية مغربية", "طاجين كفتة منزلي", "كفتة مغربية بالصلصة",
        "طاجين كفتة بالطماطم", "كفتة تقليدية بالبيض", "طاجين كفتة مغربي",
        "كفتة مغربية أصيلة", "طاجين كفتة تقليدي", "كفتة بالبيض المغربية",
        "طاجين كفتة عريق", "كفتة مغربية منزلية", "طاجين كفتة بالتوابل",
        "كفتة تقليدية أصيلة", "طاجين كفتة مغربي", "كفتة بالطماطم والبيض"
    ],
    "bissara": [
        # English queries
        "bissara moroccan split pea soup", "traditional bissara fava bean morocco", "bissara morocco green soup bowl",
        "moroccan bissara olive oil cumin", "authentic bissara traditional recipe", "bissara split pea dip morocco",
        "traditional bissara moroccan breakfast", "bissara morocco rustic bowl", "moroccan bissara green thick soup",
        "bissara fava bean traditional morocco", "bissara soup olive oil drizzle", "traditional bissara closeup bowl",
        "moroccan bissara authentic recipe", "bissara split pea moroccan cuisine", "bissara morocco food photography",
        "traditional bissara green soup", "moroccan bissara homemade dish", "bissara fava bean soup morocco",
        "bissara morocco traditional breakfast", "authentic bissara split pea", "bissara moroccan soup rustic",
        # French queries
        "bissara marocaine soupe fèves", "bissara traditionnelle pois cassés", "bissara marocaine verte épaisse",
        "bissara soupe fèves huile olive", "bissara traditionnelle petit-déjeuner maroc", "bissara marocaine recette authentique",
        "bissara fèves vertes marocaine", "bissara traditionnelle bol terre cuite", "bissara marocaine cumin huile",
        "bissara soupe pois cassés maroc", "bissara traditionnelle présentation rustique", "bissara marocaine fait maison",
        "bissara fèves traditionnelle marocaine", "bissara soupe verte épaisse", "bissara marocaine closeup photographie",
        "bissara traditionnelle cuisine marocaine", "bissara marocaine recette ancestrale", "bissara fèves huile olive",
        "bissara traditionnelle bol fumant", "bissara marocaine soupe traditionnelle", "bissara pois cassés authentique",
        # Arabic queries
        "بيصارة مغربية تقليدية", "بيصارة بالفول المغربية", "بيصارة مغربية خضراء",
        "بيصارة تقليدية مغربية", "شوربة بيصارة مغربية", "بيصارة بالفول الأخضر",
        "بيصارة مغربية بالزيت", "بيصارة تقليدية أصيلة", "بيصارة مغربية منزلية",
        "بيصارة بالكمون المغربية", "بيصارة تقليدية للفطور", "شوربة بيصارة خضراء",
        "بيصارة مغربية كثيفة", "بيصارة تقليدية بالثوم", "بيصارة بالفول تقليدية",
        "بيصارة مغربية أصيلة", "بيصارة تقليدية عريقة", "شوربة بيصارة منزلية",
        "بيصارة مغربية بالفلفل", "بيصارة تقليدية مغربية", "بيصارة بالزيت والكمون"
    ]
}

TRAIN_TARGET = 750
VAL_TARGET = 250
OUTPUT_DIR = "D:/moroccan_food_images"

print("="*70)
print("INCREMENTAL IMAGE SCRAPER - Continues from Existing Images")
print("="*70)
print(f"\nFeatures:")
print(f"  ✅ ADDS to existing images (doesn't delete)")
print(f"  ✅ Continues numbering from last image")
print(f"  ✅ Uses NEW search terms to find different images")
print(f"  ✅ Duplicate detection (skips same images)")
print(f"  ✅ Target: 750 train + 250 validation per class")
print("="*70)

# Track image hashes to avoid duplicates
image_hashes = {}

def get_image_hash(file_path):
    """Calculate hash of image to detect duplicates"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def is_duplicate(file_path, dish_name):
    """Check if image is duplicate"""
    img_hash = get_image_hash(file_path)
    if img_hash is None:
        return True  # Treat unreadable as duplicate
    
    if dish_name not in image_hashes:
        image_hashes[dish_name] = set()
    
    if img_hash in image_hashes[dish_name]:
        return True
    
    image_hashes[dish_name].add(img_hash)
    return False

def scan_existing_images(dish_name):
    """Scan existing images and get starting numbers"""
    train_path = Path(OUTPUT_DIR) / "train" / dish_name
    val_path = Path(OUTPUT_DIR) / "validation" / dish_name
    
    train_path.mkdir(parents=True, exist_ok=True)
    val_path.mkdir(parents=True, exist_ok=True)
    
    # Count existing images
    train_count = 0
    val_count = 0
    
    # Build hash set of existing images
    if dish_name not in image_hashes:
        image_hashes[dish_name] = set()
    
    for img_path in train_path.glob("*.*"):
        img_hash = get_image_hash(img_path)
        if img_hash:
            image_hashes[dish_name].add(img_hash)
            train_count += 1
    
    for img_path in val_path.glob("*.*"):
        img_hash = get_image_hash(img_path)
        if img_hash:
            image_hashes[dish_name].add(img_hash)
            val_count += 1
    
    return train_count, val_count

def is_valid_image(file_path):
    """Check if file is valid image"""
    try:
        if file_path.stat().st_size < 1000:
            return False
        img = Image.open(file_path)
        img.verify()
        return True
    except:
        return False

def download_incremental(dish_name, search_terms, current_train, current_val):
    """Download images and continue from current counts"""
    
    train_needed = TRAIN_TARGET - current_train
    val_needed = VAL_TARGET - current_val
    total_needed = train_needed + val_needed
    
    if total_needed <= 0:
        print(f"  ✅ {dish_name} already complete! ({current_train} train, {current_val} val)")
        return current_train, current_val
    
    print(f"\n{'='*70}")
    print(f"📸 {dish_name.upper()}")
    print(f"{'='*70}")
    print(f"  Current: {current_train} train, {current_val} val")
    print(f"  Need: {train_needed} train, {val_needed} val ({total_needed} total)")
    print(f"  Starting from image #{current_train + current_val + 1}")
    
    temp_folder = Path(OUTPUT_DIR) / f"temp_{dish_name}_incremental"
    collected = []
    
    for idx, search_term in enumerate(search_terms, 1):
        if len(collected) >= total_needed:
            print(f"  ✅ Target reached!")
            break
        
        remaining = total_needed - len(collected)
        print(f"\n  [{idx}/{len(search_terms)}] Search: '{search_term}'")
        print(f"      Collected: {len(collected)} | Need: {remaining}")
        
        search_folder = temp_folder / f"search_{idx}"
        search_folder.mkdir(parents=True, exist_ok=True)
        
        try:
            # Use Bing only (Google blocks automated access)
            print(f"      Using: Bing")
            crawler = BingImageCrawler(
                storage={'root_dir': str(search_folder)},
                downloader_threads=4,
                parser_threads=2
            )
            
            images_to_get = min(200, remaining + 100)
            crawler.crawl(
                keyword=search_term,
                max_num=images_to_get,
                min_size=(200, 200)
            )
            
            time.sleep(10)
            
            # Process downloaded images
            new_count = 0
            for f in search_folder.iterdir():
                if f.is_file() and is_valid_image(f):
                    # Check for duplicates
                    if not is_duplicate(f, dish_name):
                        collected.append(f)
                        new_count += 1
                    else:
                        f.unlink()  # Delete duplicate
            
            print(f"      ✓ Found {new_count} new unique images")
            
            # Small delay
            time.sleep(4)
            
        except Exception as e:
            logging.error(f"Search {idx} failed: {e}")
            continue
    
    if len(collected) == 0:
        print(f"  ⚠️  No new images found")
        if temp_folder.exists():
            shutil.rmtree(temp_folder)
        return current_train, current_val
    
    # Shuffle collected images
    random.shuffle(collected)
    
    # Split: prioritize train first
    train_to_add = min(train_needed, len(collected))
    val_to_add = min(val_needed, len(collected) - train_to_add)
    
    train_images = collected[:train_to_add]
    val_images = collected[train_to_add:train_to_add + val_to_add]
    
    print(f"\n  📦 Adding images...")
    
    # Add to train folder
    train_added = 0
    for img_file in train_images:
        try:
            new_num = current_train + train_added + 1
            new_name = f"{dish_name}_{new_num}{img_file.suffix}"
            dst = Path(OUTPUT_DIR) / "train" / dish_name / new_name
            shutil.move(str(img_file), str(dst))
            train_added += 1
        except Exception as e:
            logging.warning(f"Failed to move {img_file.name}: {e}")
    
    # Add to validation folder
    val_added = 0
    for img_file in val_images:
        try:
            new_num = current_val + val_added + 1
            new_name = f"{dish_name}_val_{new_num}{img_file.suffix}"
            dst = Path(OUTPUT_DIR) / "validation" / dish_name / new_name
            shutil.move(str(img_file), str(dst))
            val_added += 1
        except Exception as e:
            logging.warning(f"Failed to move {img_file.name}: {e}")
    
    new_train = current_train + train_added
    new_val = current_val + val_added
    
    print(f"  ✅ Added {train_added} train + {val_added} val")
    print(f"  📊 Total now: {new_train} train, {new_val} val")
    
    # Cleanup
    if temp_folder.exists():
        shutil.rmtree(temp_folder)
    
    return new_train, new_val

# Main loop
print("\n🌐 Starting incremental download...\n")

results = {}

for dish_name, search_terms in moroccan_dishes.items():
    try:
        # Scan existing
        current_train, current_val = scan_existing_images(dish_name)
        
        # Download more
        new_train, new_val = download_incremental(
            dish_name, 
            search_terms,
            current_train,
            current_val
        )
        
        results[dish_name] = (new_train, new_val)
        
        # Delay between dishes
        print(f"  ⏳ Waiting 15 seconds...\n")
        time.sleep(15)
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Interrupted!")
        # Cleanup any temp folders
        temp_folder = Path(OUTPUT_DIR) / f"temp_{dish_name}_incremental"
        if temp_folder.exists():
            print(f"  🧹 Cleaning up temp folder...")
            shutil.rmtree(temp_folder)
        break
    except Exception as e:
        print(f"  ❌ Error for {dish_name}: {e}")
        # Cleanup temp folder on error
        temp_folder = Path(OUTPUT_DIR) / f"temp_{dish_name}_incremental"
        if temp_folder.exists():
            print(f"  🧹 Cleaning up temp folder...")
            shutil.rmtree(temp_folder)
        results[dish_name] = scan_existing_images(dish_name)
        continue

# Final Summary
print("\n" + "="*70)
print("FINAL SUMMARY - INCREMENTAL RUN")
print("="*70)

total_train = 0
total_val = 0

for dish_name in moroccan_dishes.keys():
    if dish_name in results:
        train_count, val_count = results[dish_name]
    else:
        train_count, val_count = scan_existing_images(dish_name)
    
    total_train += train_count
    total_val += val_count
    total = train_count + val_count
    
    train_pct = int(train_count / TRAIN_TARGET * 100)
    val_pct = int(val_count / VAL_TARGET * 100)
    
    if train_count >= TRAIN_TARGET and val_count >= VAL_TARGET:
        status = "✅"
    elif total >= 500:
        status = "⚠️"
    else:
        status = "❌"
    
    print(f"  {status} {dish_name:12} → Train: {train_count:4}/{TRAIN_TARGET} ({train_pct}%), Val: {val_count:4}/{VAL_TARGET} ({val_pct}%)")

print(f"\n  📊 Grand Total: {total_train} train + {total_val} validation = {total_train + total_val} images")
print(f"  🎯 Final Target: {TRAIN_TARGET * 5} train + {VAL_TARGET * 5} validation = 5000 images")

overall = int((total_train + total_val) / 5000 * 100)
print(f"  📈 Overall progress: {overall}%")

if total_train + total_val >= 2500:
    print(f"\n✅ Excellent! Dataset ready for CNN/KNN training!")
    print(f"   Next: python add_custom_images.py")
elif total_train + total_val >= 1500:
    print(f"\n⚠️  Good dataset! You can:")
    print(f"   1. Run this script again to add more (it will continue)")
    print(f"   2. Or proceed with: python add_custom_images.py")
else:
    print(f"\n⚠️  Run this script again to add more images!")
    print(f"   It will continue from where it stopped.")

print("="*70)
