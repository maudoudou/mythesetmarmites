/* ==========================================================================
   Mythes & Marmites — routage, filtres, parutions
   ========================================================================== */

/* ---------------------------- Les parutions ---------------------------- */
const CATS = [
  { id: 'tout',   label: 'Tout' },
  { id: 'contes', label: 'Contes' },
  { id: 'mythes', label: 'Mythes & fables' },
  { id: 'albums', label: 'Albums & romans' },
  { id: 'notes',  label: 'Notes de lecture' }
];

const ARTICLES = [
  /* ------------------------------ CONTES ------------------------------ */
  {
    slug: 'pain-poule-rousse', cat: 'contes', type: 'recette',
    kicker: 'CONTE · 25 MIN + REPOS', source: 'Conte · La Petite Poule rousse',
    title: 'Le pain de la Petite Poule rousse',
    chapeau: "Un pain lent, à faire la veille, pour vérifier une chose : qui vient aider avant que ça sente bon.",
    resume: "Personne ne veut aider à moudre le grain, mais tout le monde arrive quand le pain sort du four. Un levain à quatre mains.",
    ill: 'poule-rousse-orange', date: '12 août 2026', foot: '4 à 6 parts · 12 août',
    meta: ['25 min de travail', '12 h de repos', '4 à 6 parts'],
    photo: 'Le pain de la poule rousse, encore chaud, sur un linge',
    img: '/images/photos/pain-poule-rousse-web.jpg',
    ing: ['500 g de farine de blé T80', '10 g de sel fin', "350 g d'eau tiède", '1 c. à s. de miel', '100 g de levain liquide', 'Un peu de son pour le linge'],
    steps: [
      "Mélangez farine et eau du bout des doigts, sans travailler. Laissez reposer 30 minutes : la farine boit toute seule.",
      "Ajoutez le levain, le miel, puis le sel. Repliez la pâte sur elle-même six fois, à dix minutes d'intervalle.",
      "Couvrez et oubliez au frais toute la nuit. C'est le moment de raconter le conte ; il dure exactement le temps d'un rangement de cuisine.",
      "Le matin, façonnez une boule, laissez-la reprendre une heure sur un linge fariné.",
      "Four très chaud, 240 °C, avec un ramequin d'eau. 20 minutes, puis 20 minutes à 210 °C. Le pain doit sonner creux sous les doigts."
    ],
    enfants: "Le repliage de l'étape 2 : six gestes, six paroles. À chaque pli, celui qui plie ajoute une phrase à l'histoire. Le pain lève, le récit aussi.",
    recit: [
      "La poule trouve un grain de blé. Elle demande : qui veut m'aider à le semer ? Le chat dort, le rat bâille, le cochon a autre chose à faire. Elle sème seule, moud seule, pétrit seule. Puis le pain sort du four, et la cuisine se remplit.",
      "On lit souvent ce conte comme une leçon sur l'effort. Il dit surtout quelque chose du travail invisible : celui qu'on ne voit qu'au moment où il devient bon à manger. Dans les versions anglaises du XIX<sup>e</sup> siècle, la poule mange le pain seule ; dans beaucoup de rééditions françaises récentes, elle partage. Le conte a changé d'avis en cent ans — ça mérite qu'on en parle à table."
    ],
    question: "« Qui a travaillé pour ce qu'on est en train de manger ? »",
    lectures: ['« La Petite Poule rousse », Byron Barton, L\'École des loisirs.', 'Nicole Belmont, <em>Poétique du conte</em>, Gallimard.']
  },
  {
    slug: 'galette-sarrasin', cat: 'contes', type: 'recette',
    kicker: 'CONTE · 30 MIN', source: 'Conte · Roule galette',
    title: "La galette qui ne voulait pas être mangée",
    chapeau: "Sarrasin, beurre demi-sel, et la fuite comme moteur de récit : une galette qu'on rattrape de justesse.",
    resume: "Sarrasin, beurre demi-sel, et la fuite comme moteur de récit.",
    ill: 'roule-galette-violet', date: '1er juillet 2026', foot: '4 parts · 1er juillet',
    meta: ['15 min de travail', '15 min de cuisson', '4 parts'],
    photo: "La galette dorée sur le rebord de la fenêtre",
    img: '/images/photos/galette-web.jpg',
    ing: ['150 g de farine de sarrasin', '100 g de farine de froment', '80 g de beurre demi-sel', '1 œuf', '2 c. à s. de crème fraîche', 'Une pincée de sucre'],
    steps: [
      "Sablez les deux farines avec le beurre froid, du bout des doigts, jusqu'à obtenir un gros sable.",
      "Ajoutez l'œuf et la crème, rassemblez sans pétrir. La pâte doit rester un peu rustique.",
      "Étalez en un disque épais, dessinez une croix au couteau, dorez.",
      "25 minutes à 190 °C. Laissez tiédir sur le rebord de la fenêtre, comme dans le conte — mais surveillez le renard."
    ],
    enfants: "C'est eux qui dessinent le visage de la galette au couteau, avant la cuisson. Elle sortira du four en souriant, ou en fronçant les sourcils.",
    recit: [
      "La galette s'échappe pour ne pas être mangée. Elle chante sa chanson au lièvre, au loup, à l'ours — tous se laissent distraire. Le renard, lui, fait semblant d'être sourd, et demande qu'on chante plus près.",
      "Le conte tourne autour d'une même idée : celui qui écoute vraiment est aussi celui qui mange. La chanson est une monnaie, la vanité un piège. C'est un des rares contes où le héros se perd en se racontant trop bien."
    ],
    question: "« Quel est le plus beau moment de ta journée ? »",
    lectures: ['« Roule galette », Natha Caputo &amp; Pierre Belvès, Père Castor.', 'Vladimir Propp, <em>Morphologie du conte</em>, Seuil.']
  },
  {
    slug: 'soupe-trois-cochons', cat: 'contes', type: 'recette',
    kicker: 'CONTE · 1 H 30', source: 'Conte · Les Trois Petits Cochons',
    title: 'La soupe des trois petits cochons',
    chapeau: "Un potage de légumes racines qui tient debout, même quand le loup souffle.",
    resume: "Un potage de légumes racines qui tient debout, même quand le loup souffle.",
    ill: 'trois-petits-cochons-green', date: '3 juin 2026', foot: '6 parts · 3 juin',
    meta: ['20 min de travail', '1 h de cuisson', '6 parts'],
    photo: "La soupe en cocotte, trois bols dépareillés",
    img: '/images/photos/soupe-web.jpg',
    ing: ['3 carottes', '1 panais', '1 céleri-rave', '1 oignon jaune', '2 belles tomates', 'Un bouquet de basilic'],
    steps: [
      "Taillez tous les légumes en gros cubes.",
      "Faites-les colorer dans la graisse chaude, sans les remuer trop souvent.",
      "Couvrez d'eau à hauteur, ajoutez le basilic, laissez frémir une heure à découvert.",
      "Mixez : il faut que ça résiste encore un peu sous la cuillère."
    ],
    enfants: "Souffler sur sa cuillère, très fort, comme le loup.",
    recit: [
      "Trois maisons, trois façons de faire : vite, à peu près, ou pour longtemps. Le conte donne raison à la lenteur : et c'est une leçon qui vaut aussi pour un bouillon.",
      "Ce qui est plus étrange, c'est la fin des versions anciennes : le loup finit dans la marmite. Le prédateur devient repas. Toute une série de contes fonctionnent comme ça : on ne gagne pas contre le loup, on l'invite malgré lui à table."
    ],
    question: "« Est-ce la soupe fait réellement grandir ?»",
    lectures: ['« Les Trois Petits Cochons », Joseph Jacobs (version de 1890).', 'Bruno Bettelheim, <em>Psychanalyse des contes de fées</em>, Pocket.']
  },
  {
    slug: 'pain-epices-hansel', cat: 'contes', type: 'recette',
    kicker: 'CONTE · 50 MIN', source: 'Conte · Hansel et Gretel',
    title: "Le pain d'épices qu'on ne grignote pas en chemin",
    chapeau: "Miel de sarrasin, seigle, beaucoup de cannelle : la maison de la sorcière, en version comestible et sans piège.",
    resume: "Miel de sarrasin, seigle et cannelle : la maison de la sorcière, en version sans piège.",
    ill: 'hansel-et-gretel-orange', date: '20 mai 2026', foot: '8 parts · 20 mai',
    meta: ['20 min de travail', '50 min de cuisson', '8 parts'],
    photo: "Le pain d'épices démoulé, encore chaud",
    img: '/images/photos/pain-epices-web.jpg',
    ing: ['250 g de farine de seigle', '200 g de miel de sarrasin', '10 cl de lait', '2 c. à c. de cannelle', '1 c. à c. de gingembre moulu', '1 sachet de levure chimique'],
    steps: [
      "Faites tiédir le miel avec le lait, sans bouillir.",
      "Mélangez farine, épices et levure, versez le liquide chaud dessus, remuez vite.",
      "Versez dans un moule à cake beurré, lissez la surface à la cuillère mouillée.",
      "50 minutes à 160 °C. Attendez le lendemain pour trancher : le pain d'épices ment quand il est chaud."
    ],
    enfants: "Ils sèment des miettes sur la table pendant que ça cuit, et retracent le chemin du retour. Puis on les mange : les miettes, pas les enfants.",
    recit: [
      "Deux enfants perdus, une maison en gâteau, une faim qui devient piège. C'est le conte le plus alimentaire du répertoire : on y mange la maison avant que la maison ne vous mange.",
      "La disette est le vrai moteur de l'histoire. Les versions de 1812 sont d'ailleurs plus dures que celles de 1857 : c'est la mère, et non une marâtre, qui décide d'abandonner. Grimm a adouci au fil des éditions ce que ses lecteurs supportaient de moins en moins."
    ],
    question: "« Qu'est-ce qu'on ferait s'il ne restait rien dans les placards ? »",
    lectures: ['Jacob &amp; Wilhelm Grimm, <em>Contes pour les enfants et la maison</em>, José Corti.', 'Marina Warner, <em>Sortilèges et sorcières</em>, Le Seuil.']
  },

  /* -------------------------- MYTHES & FABLES -------------------------- */
  {
    slug: 'sanglier-gaulois', cat: 'mythes', type: 'recette',
    kicker: 'MYTHE · 2 H AU FOUR', source: 'Mythe · Le banquet gaulois',
    title: 'Le sanglier du village gaulois',
    chapeau: "Rôti au miel et au genièvre — et pourquoi le banquet clôt toujours l'album.",
    resume: "Rôti au miel et au genièvre, pour comprendre pourquoi tout album finit par un banquet.",
    ill: 'asterix-orange', date: '29 juillet 2026', foot: '6 à 8 parts · 29 juillet',
    meta: ['30 min de travail', '2 h au four', '6 à 8 parts'],
    photo: "Le rôti sur une planche, entier, avant le découpage",
    ing: ["1,5 kg d'échine de porc", '3 c. à s. de miel de forêt', '10 baies de genièvre', '2 oignons', '25 cl de cidre brut', 'Gros sel, poivre concassé'],
    steps: [
      "Frottez la viande de gros sel, poivre et genièvre écrasé. Laissez-la respirer une heure hors du froid.",
      "Saisissez-la de tous côtés dans une cocotte très chaude, puis ajoutez les oignons en quartiers.",
      "Déglacez au cidre, badigeonnez de miel, couvrez.",
      "2 h à 150 °C, en arrosant toutes les 20 minutes. Servez à la table entière, dans le plat de cuisson."
    ],
    enfants: "Ce sont eux qui arrosent, toutes les vingt minutes et qui annoncent chaque fois, à voix haute, combien de temps il reste avant le banquet.",
    recit: [
      "Dans presque tous les albums d'Astérix, la dernière case est un banquet. Le village se rassemble, on partage le sanglier, et le seul exclu est celui qui ne sait pas se taire.",
      "C'est une structure de récit très ancienne. Le festin final scelle le retour à l'ordre, comme les noces à la fin des contes. On ne raconte pas que l'aventure est finie, on la mange."
    ],
    question: "« Qu'est-ce qu'on fête, là, exactement ? »",
    lectures: ['René Goscinny &amp; Albert Uderzo, <em>Astérix le Gaulois</em>, Dargaud.', 'Florence Dupont, <em>Le Plaisir et la loi</em>, La Découverte.']
  },
  {
    slug: 'fromage-corbeau', cat: 'mythes', type: 'recette',
    kicker: 'FABLE · 20 MIN', source: 'Fable · Le Corbeau et le Renard',
    title: 'Le fromage du corbeau',
    chapeau: "Toast chaud au comté et miel, à manger avant de se faire flatter.",
    resume: "Toast chaud au comté et miel, à manger avant de se faire flatter.",
    ill: 'corbeau-renard-violet', date: '6 mai 2026', foot: '4 parts · 6 mai',
    meta: ['10 min de travail', '10 min de cuisson', '4 parts'],
    photo: "Les toasts sortant du four, le fromage encore bouillonnant",
    ing: ['4 tranches de pain de campagne', '200 g de comté 18 mois', '2 c. à c. de miel de châtaignier', 'Quelques noix', 'Poivre du moulin', 'Un peu de beurre'],
    steps: [
      "Beurrez le pain, couvrez-le de lamelles de comté épaisses.",
      "Passez 8 minutes sous le gril, jusqu'à ce que le fromage boursoufle.",
      "Filet de miel, noix concassées, poivre. À manger tout de suite, sans le lâcher."
    ],
    enfants: "Chacun doit faire un compliment exagéré à son voisin avant de croquer. Si le voisin ouvre la bouche pour répondre… il perd son toast (une seconde seulement).",
    recit: [
      "Le corbeau tient son fromage, le renard tient son discours. La fable est courte parce que le piège est simple : on ne perd pas le fromage, on le lâche soi-même en ouvrant le bec.",
      "La Fontaine s'amuse à faire de la flatterie une technique de cuisine. Ce que la fable dit vraiment, c'est que la parole n'est pas gratuite : parler coûte quelque chose, et parfois, c'est le repas."
    ],
    question: "« Est-ce qu'on t'a déjà fait un compliment intéressé ? »",
    lectures: ['Jean de La Fontaine, <em>Fables</em>, livre I.', 'Ésope, <em>Fables</em>, traduction de Daniel Loayza, GF.']
  },
  {
    slug: 'potion-panoramix', cat: 'mythes', type: 'recette',
    kicker: 'MYTHE · 25 MIN', source: 'Mythe · La potion du druide',
    title: "La tisane du druide (qui ne rend pas invincible)",
    chapeau: "Gui, verveine, un peu de gingembre : une infusion qui réchauffe assez pour qu'on se croie plus fort.",
    resume: "Verveine, gingembre, écorce d'orange : une infusion qui réchauffe assez pour qu'on se croie plus fort.",
    ill: 'marmite-violet', date: '22 avril 2026', foot: '1 litre · 22 avril',
    meta: ['10 min de travail', '15 min d\'infusion', '1 litre'],
    photo: "La marmite fumante, les herbes séchées à côté",
    ing: ['1 litre d\'eau de source', 'Une grosse poignée de verveine séchée', '3 rondelles de gingembre frais', 'Le zeste d\'une orange', '1 c. à s. de miel de bruyère', 'Une pincée de poivre long'],
    steps: [
      "Portez l'eau juste avant l'ébullition — jamais bouillante, les herbes se vexent.",
      "Jetez-y verveine, gingembre et zeste, couvrez, comptez 15 minutes.",
      "Filtrez, sucrez au miel, poivrez très légèrement. Servez dans des bols, avec beaucoup de sérieux."
    ],
    enfants: "Chacun ajoute un ingrédient imaginaire à la marmite en annonçant son pouvoir. On note tout : c'est la recette de la potion de la maison.",
    recit: [
      "Le druide qui prépare seul, à l'écart, une décoction dont personne ne connaît la formule : la figure traverse les mythes celtiques bien avant la bande dessinée. Le secret fait partie de la recette.",
      "Ce qui compte, dans ces récits, c'est moins l'effet que le rituel : la marmite, l'attente, la distribution mesurée. On boit une histoire autant qu'un liquide — et un bol de tisane bien annoncé fait, chez les enfants, à peu près le même effet."
    ],
    question: "« De quoi aurais-tu besoin, ce soir, pour te sentir invincible ? »",
    lectures: ['Françoise Le Roux &amp; Christian-J. Guyonvarc\'h, <em>Les Druides</em>, Ouest-France.', 'Claude Sterckx, <em>Mythologie du monde celte</em>, Marabout.']
  },
  {
    slug: 'pommes-idunn', cat: 'mythes', type: 'recette',
    kicker: 'MYTHE · 40 MIN', source: 'Mythe · Les pommes d\'Idunn',
    title: "Les pommes d'Idunn, cuites au beurre salé",
    chapeau: "Les dieux du Nord doivent leur jeunesse à un panier de pommes. Voici la version poêlée, avec de la crème épaisse.",
    resume: "Les dieux du Nord doivent leur jeunesse à un panier de pommes. Version poêlée, crème épaisse.",
    ill: 'alice-orange', date: '8 avril 2026', foot: '4 parts · 8 avril',
    meta: ['15 min de travail', '25 min de cuisson', '4 parts'],
    photo: "Les pommes caramélisées dans la poêle en fonte",
    ing: ['6 pommes à cuire', '60 g de beurre demi-sel', '3 c. à s. de sucre de canne', '1 gousse de vanille', '10 cl de crème épaisse', 'Une pincée de cardamome'],
    steps: [
      "Coupez les pommes en quartiers épais, sans les peler.",
      "Faites mousser le beurre, jetez les pommes, laissez-les colorer sans y toucher trois bonnes minutes.",
      "Sucrez, ajoutez la vanille fendue, secouez la poêle plutôt que de remuer.",
      "Hors du feu, crème épaisse et cardamome. Servez dans la poêle, au centre de la table."
    ],
    enfants: "Un quartier chacun, les yeux fermés, et il faut deviner l'épice. Celui qui trouve raconte ce qu'il ferait avec la jeunesse éternelle.",
    recit: [
      "Idunn garde les pommes qui maintiennent les dieux jeunes. Quand Loki la fait enlever, les dieux vieillissent d'un coup : la mythologie nordique fait dépendre l'immortalité d'un panier de fruits, et d'une femme qui le porte.",
      "C'est un motif qu'on retrouve partout : le fruit qui prolonge la vie, le jardin qu'il faut garder, le vol qui déclenche la catastrophe. Chez Grimm comme chez Snorri, ce qui se mange fait basculer le récit."
    ],
    question: "« Qu'est-ce que tu voudrais garder exactement comme c'est aujourd'hui ? »",
    lectures: ['Snorri Sturluson, <em>L\'Edda</em>, traduction François-Xavier Dillmann, Gallimard.', 'Régis Boyer, <em>La Grande Déesse du Nord</em>, Berg International.']
  },

  /* -------------------------- ALBUMS & ROMANS -------------------------- */
  {
    slug: 'tartelettes-mange-moi', cat: 'albums', type: 'recette',
    kicker: 'ALBUM · 40 MIN', source: 'Roman · Alice au pays des merveilles',
    title: 'Les tartelettes « mange-moi »',
    chapeau: "Confiture de framboise, pâte sablée, et la nourriture comme machine à métamorphoses.",
    resume: "Pâte sablée, framboise, et la nourriture comme machine à métamorphoses.",
    ill: 'alice-green', date: '15 juillet 2026', foot: '12 pièces · 15 juillet',
    meta: ['25 min de travail', '15 min de cuisson', '12 pièces'],
    photo: "Les tartelettes alignées, l'étiquette « mange-moi » posée dessus",
    ing: ['250 g de farine', '125 g de beurre froid', '80 g de sucre glace', '1 jaune d\'œuf', '200 g de confiture de framboise', 'Un peu de sucre grain'],
    steps: [
      "Sablez farine, beurre et sucre glace, liez au jaune d'œuf. Reposez la pâte 30 minutes au frais.",
      "Étalez fin, foncez douze empreintes, piquez le fond.",
      "Une cuillère de confiture dans chacune, une bande de pâte en croix par-dessus.",
      "15 minutes à 180 °C. Écrivez « mange-moi » sur une étiquette et posez-la sur le plat : c'est la moitié de la recette."
    ],
    enfants: "Chacun dessine son étiquette : « mange-moi », « bois-moi », « surtout pas moi ». On échange les assiettes sans regarder.",
    recit: [
      "Alice ne cesse pas de manger et de boire, et chaque bouchée change sa taille. Le gâteau qui fait grandir, la fiole qui fait rétrécir : le corps devient un problème de mesure.",
      "Carroll fait de la nourriture un moteur narratif pur. Ce n'est pas un plaisir, c'est une transformation — et c'est exactement ce que les enfants savent d'instinct : on grandit en mangeant, et ça n'est jamais complètement rassurant."
    ],
    question: "« Si un gâteau te faisait grandir d'un coup, tu le mangerais ? »",
    lectures: ['Lewis Carroll, <em>Les Aventures d\'Alice au pays des merveilles</em>, GF.', 'Jean-Jacques Lecercle, <em>Philosophy of Nonsense</em>, Routledge.']
  },
  {
    slug: 'carottes-monsieur-lapin', cat: 'albums', type: 'recette',
    kicker: 'ALBUM · 35 MIN', source: 'Album · Monsieur Lapin',
    title: 'Les carottes de Monsieur Lapin',
    chapeau: "Rôties au four avec du cumin, mangées avec les doigts. Un plat pour ceux qui posent trop de questions.",
    resume: "Rôties au four avec du cumin, mangées avec les doigts, par ceux qui posent trop de questions.",
    ill: 'monsieur-lapin-orange', date: '25 mars 2026', foot: '4 parts · 25 mars',
    meta: ['10 min de travail', '35 min au four', '4 parts'],
    photo: "Les carottes rôties dans le plat, fanes comprises",
    ing: ['1 kg de carottes avec fanes', '3 c. à s. d\'huile d\'olive', '1 c. à c. de cumin en grains', '1 c. à c. de miel', '1 citron', 'Fleur de sel'],
    steps: [
      "Lavez les carottes sans les peler, gardez 2 cm de fanes.",
      "Roulez-les dans l'huile, le cumin, le miel et le zeste de citron.",
      "35 minutes à 200 °C, en les retournant à mi-parcours.",
      "Jus de citron à la sortie, fleur de sel, et on mange avec les doigts."
    ],
    enfants: "Une question chacun, à tour de table, avant de prendre une carotte. Les questions bêtes comptent double.",
    recit: [
      "Monsieur Lapin passe l'album à demander aux autres animaux de quelle couleur est le temps. Personne ne répond pareil. Il n'y a pas de bonne réponse, et c'est le sujet du livre.",
      "Les albums qui marchent avec les plus jeunes fonctionnent souvent comme ça : une question répétée, une série de réponses, et un lecteur qui prend le rythme. À table, la mécanique se transpose sans effort."
    ],
    question: "« De quelle couleur était ta journée ? »",
    lectures: ['« Monsieur Lapin », album jeunesse (série).', 'Sophie Van der Linden, <em>Lire l\'album</em>, L\'Atelier du poisson soluble.']
  },
  {
    slug: 'bouillie-ours', cat: 'albums', type: 'recette',
    kicker: 'CONTE ILLUSTRÉ · 15 MIN', source: 'Conte · Boucle d\'or et les trois ours',
    title: "La bouillie qui n'est ni trop chaude ni trop froide",
    chapeau: "Flocons d'avoine, lait entier, une pointe de sel : trois bols, trois températures, et la bonne mesure comme sujet.",
    resume: "Trois bols, trois températures, et la bonne mesure comme sujet du repas.",
    ill: 'ours-boucle-dor-green', date: '10 mars 2026', foot: '3 bols · 10 mars',
    meta: ['5 min de travail', '10 min de cuisson', '3 bols'],
    photo: "Trois bols dépareillés, du plus grand au plus petit",
    ing: ['120 g de flocons d\'avoine', '50 cl de lait entier', 'Une pincée de sel', '1 c. à s. de cassonade', 'Une noisette de beurre', 'Quelques amandes'],
    steps: [
      "Portez le lait salé à frémissement, versez les flocons en pluie.",
      "Remuez 8 minutes à feu doux : la bouillie doit napper la cuillère.",
      "Beurre, cassonade, amandes. Répartissez dans trois bols de tailles différentes et laissez-les attendre — c'est le cœur du conte."
    ],
    enfants: "Chacun goûte les trois bols et dit lequel est le sien. Personne n'a le droit de s'asseoir avant d'avoir choisi sa chaise.",
    recit: [
      "Boucle d'or entre, goûte, casse, dort. Le conte est une leçon de mesure racontée par une transgression : il faut essayer les trois bols pour savoir ce qui convient.",
      "C'est aussi l'un des rares récits pour enfants entièrement construit sur le mobilier et la vaisselle. Les objets du quotidien y font le récit — et c'est pour ça qu'il fonctionne si bien dès trois ans."
    ],
    question: "« C'est quoi, pour toi, la bonne quantité ? »",
    lectures: ['Robert Southey, « The Story of the Three Bears » (1837).', 'Christian Bruel, <em>Les Images de l\'enfance</em>, Être.']
  },
  {
    slug: 'epinards-popeye', cat: 'albums', type: 'recette',
    kicker: 'BANDE DESSINÉE · 20 MIN', source: 'Bande dessinée · Popeye',
    title: 'Les épinards qui rendent fort (ou presque)',
    chapeau: "À la crème et à l'ail, loin de la boîte de conserve — et la vraie histoire de l'erreur de calcul du fer.",
    resume: "À la crème et à l'ail, loin de la conserve — et la vraie histoire de l'erreur sur le fer.",
    ill: 'popeye-green', date: '18 février 2026', foot: '4 parts · 18 février',
    meta: ['10 min de travail', '10 min de cuisson', '4 parts'],
    photo: "La poêle d'épinards, la gousse d'ail à côté",
    ing: ['1 kg d\'épinards frais', '2 gousses d\'ail', '20 cl de crème fraîche', 'Une râpée de muscade', '30 g de beurre', 'Sel, poivre'],
    steps: [
      "Lavez les épinards trois fois. Oui, trois.",
      "Faites-les tomber par poignées dans le beurre chaud avec l'ail écrasé.",
      "Égouttez franchement, remettez sur le feu avec la crème, deux minutes.",
      "Muscade, poivre. Servez brûlant, avec un œuf mollet si la tablée a faim."
    ],
    enfants: "Contracter le biceps après la première bouchée, tous en même temps. Puis vérifier si ça marche vraiment.",
    recit: [
      "Popeye a fait manger des épinards à des générations d'enfants sur la base d'une erreur : une virgule mal placée dans une analyse du XIX<sup>e</sup> siècle a longtemps multiplié par dix leur teneur en fer.",
      "L'histoire est belle même corrigée : elle montre qu'un personnage peut changer les habitudes alimentaires d'un pays. Ce qui se raconte finit dans les assiettes — ce qui est, exactement, le pari de ce site."
    ],
    question: "« Qu'est-ce que tu as commencé à aimer à cause d'une histoire ? »",
    lectures: ['E. C. Segar, <em>Popeye</em>, planches de 1929-1938.', 'Mike Sutton, « Spinach, Iron and Popeye », <em>Internet Journal of Criminology</em>.']
  },

  /* -------------------------- NOTES DE LECTURE -------------------------- */
  {
    slug: 'faim-dans-les-contes', cat: 'notes', type: 'note',
    kicker: 'NOTES DE LECTURE', source: 'Notes · Recherche en cours',
    title: 'Ce que mangent les enfants dans les contes',
    chapeau: "Trois pages de notes sur la faim, la forêt et le pain — les premières briques de ma recherche.",
    resume: "Trois pages de notes sur la faim, la forêt et le pain — les premières briques de ma recherche.",
    ill: 'carotte-orange', date: '17 juin 2026', foot: 'Lecture 8 min · 17 juin',
    meta: ['Lecture 8 min', 'Notes de terrain'],
    photo: "La pile de livres du moment, sur la table de travail",
    corps: [
      "J'ai relu vingt contes en cherchant une seule chose : ce que les personnages mangent, et à quel moment. Le résultat tient en une observation simple. Dans la première moitié du récit, on a faim. Dans la seconde, on mange — et le repas dit toujours que quelque chose est réglé.",
      "La faim n'est presque jamais décrite. Elle est posée comme un fait : la famine, la disette, le placard vide. Ce sont les récits eux-mêmes qui sont sobres : trois mots suffisent à installer le manque, alors que le banquet final s'étale sur des paragraphes. La rareté ne se raconte pas, l'abondance se déploie.",
      "Deuxième observation, plus troublante : dans les contes, manger est presque toujours une prise de risque. La pomme, la maison en pain d'épices, le gâteau qui fait grandir. Accepter la nourriture d'un inconnu, c'est entrer dans son histoire. On enseigne aux enfants la prudence par la bouche."
    ],
    question: "« Est-ce qu'on peut avoir confiance en quelqu'un qui nous nourrit ? »",
    lectures: ['Nicole Belmont, <em>Poétique du conte</em>, Gallimard.', 'Marina Warner, <em>Sortilèges et sorcières</em>, Le Seuil.', 'Catherine Velay-Vallantin, <em>L\'Histoire des contes</em>, Fayard.']
  },
  {
    slug: 'foret-pain-peur', cat: 'notes', type: 'note',
    kicker: 'NOTES DE LECTURE', source: 'Notes · Recherche en cours',
    title: 'La forêt, le pain, et la peur',
    chapeau: "Pourquoi les enfants des contes emportent toujours quelque chose à manger avant de se perdre.",
    resume: "Pourquoi les enfants des contes emportent toujours quelque chose à manger avant de se perdre.",
    ill: 'chaperon-rouge-violet', date: '2 juin 2026', foot: 'Lecture 6 min · 2 juin',
    meta: ['Lecture 6 min', 'Notes de terrain'],
    photo: "Un panier, un torchon, un morceau de pain",
    corps: [
      "Le Petit Chaperon rouge part avec une galette et un petit pot de beurre. Hansel emporte du pain. Le Petit Poucet, des cailloux — mais il a d'abord voulu des miettes. Avant chaque entrée en forêt, il y a un paquet de nourriture.",
      "Ce paquet a deux fonctions. Il dit que la maison existe encore, quelque part derrière ; et il devient l'objet que le prédateur convoite. Le loup demande où va la galette avant de demander où va l'enfant. La nourriture est le fil qui relie le foyer au danger.",
      "J'y vois une raison de continuer à cuisiner avec les récits plutôt qu'à côté d'eux. Le panier du Chaperon n'est pas un décor : c'est le nœud de l'histoire. Le refaire — vraiment, avec de la farine et du beurre — remet l'enfant du côté de celui qui prépare, pas seulement de celui qui écoute."
    ],
    question: "« Qu'est-ce que tu emporterais, toi, pour traverser la forêt ? »",
    lectures: ['Charles Perrault, <em>Contes</em>, édition de Jean-Pierre Collinet, Gallimard.', 'Yvonne Verdier, « Grands-mères, si vous saviez », <em>Le Débat</em>.', 'Bruno Bettelheim, <em>Psychanalyse des contes de fées</em>, Pocket.']
  },
  {
    slug: 'banquet-fin-heureuse', cat: 'notes', type: 'note',
    kicker: 'NOTES DE LECTURE', source: 'Notes · Recherche en cours',
    title: 'Le banquet comme fin heureuse',
    chapeau: "Noces, festins, tablées : pourquoi les histoires se terminent si souvent par un repas, et ce que ça dit du lecteur.",
    resume: "Noces, festins, tablées : pourquoi les histoires finissent par un repas.",
    ill: 'livre-violet', date: '14 mai 2026', foot: 'Lecture 7 min · 14 mai',
    meta: ['Lecture 7 min', 'Notes de terrain'],
    photo: "Une longue table dressée, vue de bout",
    corps: [
      "« Et l'on fit un grand festin qui dura trois jours. » La formule revient si souvent qu'on ne la lit plus. Elle fait pourtant un travail précis : elle ferme le récit sans avoir besoin de conclure quoi que ce soit.",
      "Le banquet est une fin commode parce qu'il rassemble tout le monde, y compris les personnages secondaires qu'on avait laissés en route. C'est un dispositif de récit, pas une récompense : il donne à voir la communauté reconstituée. La table est le lieu où le conte vérifie que plus personne ne manque.",
      "C'est aussi, très concrètement, ce qui m'a menée à faire un jeu qui se joue à table. Si les histoires finissent par des repas, autant commencer par là : mettre les gens dans la position de la dernière page, et voir ce qu'ils inventent."
    ],
    question: "« Qui manque à cette table, ce soir ? »",
    lectures: ['Vladimir Propp, <em>Morphologie du conte</em>, Seuil.', 'Florence Dupont, <em>Le Plaisir et la loi</em>, La Découverte.', 'Michel Jeanneret, <em>Des mets et des mots</em>, José Corti.']
  },
  {
    slug: 'gouter-des-albums', cat: 'notes', type: 'note',
    kicker: 'NOTES DE LECTURE', source: 'Notes · Recherche en cours',
    title: "Le goûter, ce format d'album",
    chapeau: "Ce que les albums du soir doivent aux quinze minutes qui suivent l'école.",
    resume: "Ce que les albums du soir doivent aux quinze minutes qui suivent l'école.",
    ill: 'souris-green', date: '28 avril 2026', foot: 'Lecture 5 min · 28 avril',
    meta: ['Lecture 5 min', 'Notes de terrain'],
    photo: "Un album ouvert à côté d'un bol et d'une tartine",
    corps: [
      "Un album se lit en huit minutes. Un goûter dure un quart d'heure. Ce n'est pas une coïncidence : les deux formats se sont ajustés l'un à l'autre, dans les cuisines, bien avant d'être théorisés.",
      "Ce que ça change pour qui fabrique des livres : le rythme des pages doit tenir la main occupée. Une double page trop bavarde perd l'enfant qui mâche ; une page trop maigre lui laisse le temps de partir. Les meilleurs albums sont réglés sur une respiration très physique.",
      "Je note ça parce que ça vaut aussi pour un jeu, un menu, un livret d'exposition. Un imprimé n'est jamais lu dans le vide : il est lu debout, assis, la bouche pleine. C'est un paramètre de fabrication, pas un détail."
    ],
    question: "« Combien de temps dure vraiment votre goûter ? »",
    lectures: ['Sophie Van der Linden, <em>Lire l\'album</em>, L\'Atelier du poisson soluble.', 'Isabelle Nières-Chevrel, <em>Introduction à la littérature de jeunesse</em>, Didier.']
  }
];

/* ---------------------------- Utilitaires ---------------------------- */
const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const catLabel = id => (CATS.find(c => c.id === id) || {}).label || '';
const countOf  = id => id === 'tout' ? ARTICLES.length : ARTICLES.filter(a => a.cat === id).length;
const listOf   = id => id === 'tout' ? ARTICLES.slice() : ARTICLES.filter(a => a.cat === id);
const PER_PAGE = 3;

/* Dimensions intrinsèques des illustrations (identiques pour une couleur et
   sa variante -cream), pour poser des attributs width/height corrects et
   éviter un saut de mise en page au chargement. */
const ILL_DIMS = {
  'poule-rousse-orange': [87, 125], 'roule-galette-violet': [241, 164],
  'trois-petits-cochons-green': [262, 190], 'hansel-et-gretel-orange': [193, 139],
  'asterix-orange': [88, 164], 'corbeau-renard-violet': [717, 1129],
  'marmite-violet': [140, 91], 'alice-orange': [128, 203], 'alice-green': [128, 203],
  'monsieur-lapin-orange': [95, 165], 'ours-boucle-dor-green': [251, 115],
  'popeye-green': [188, 204], 'carotte-orange': [68, 216],
  'chaperon-rouge-violet': [163, 143], 'livre-violet': [112, 169], 'souris-green': [102, 141]
};
function illAttrs(name) {
  const d = ILL_DIMS[name];
  return d ? ` width="${d[0]}" height="${d[1]}"` : '';
}

/* ---------------------------- Vignettes ---------------------------- */
function cardHTML(a) {
  const kick = a.cat === 'contes' ? '' : a.cat === 'mythes' ? ' card__kicker--green' : ' card__kicker--violet';
  return `<article class="contents"><a class="card card--r16 card--link" href="/a-table/${a.slug}">
    <img class="card__ill" src="/images/${a.ill}.svg" alt=""${illAttrs(a.ill)} loading="lazy" style="width:100%;height:120px;object-fit:contain">
    <p class="card__kicker${kick}" style="margin-top:20px">${a.kicker}</p>
    <h3 class="card__title" style="margin:8px 0 10px">${a.title}</h3>
    <p class="card__text" style="margin-bottom:14px">${a.resume}</p>
    <p class="small" style="font-size:13px">${a.foot}</p>
  </a></article>`;
}

/* ---------------------------- « À table » ---------------------------- */
let state = { cat: 'tout', page: 1 };

function renderFilters() {
  $('#filters').innerHTML = CATS.map(c =>
    `<button class="chip${c.id === state.cat ? ' is-on' : ''}" data-cat="${c.id}" role="tab" aria-selected="${c.id === state.cat}">${c.label} <span class="chip__n">${countOf(c.id)}</span></button>`
  ).join('');
}

function renderList() {
  const items = listOf(state.cat);
  const pages = Math.max(1, Math.ceil(items.length / PER_PAGE));
  state.page = Math.min(state.page, pages);
  const start = (state.page - 1) * PER_PAGE;
  const slice = items.slice(start, start + PER_PAGE);

  $('#results-count').textContent =
    `${items.length} parution${items.length > 1 ? 's' : ''} — ${state.cat === 'tout' ? 'toutes rubriques' : catLabel(state.cat).toLowerCase()} · page ${state.page} sur ${pages}`;
  $('#list').innerHTML = slice.map(cardHTML).join('');

  const btn = (label, page, on, dis) =>
    `<button class="pager__b${on ? ' is-on' : ''}" data-page="${page}"${dis ? ' disabled' : ''}>${label}</button>`;
  let html = btn('←', state.page - 1, false, state.page === 1);
  for (let i = 1; i <= pages; i++) html += btn(i, i, i === state.page, false);
  html += btn('→', state.page + 1, false, state.page === pages);
  $('#pager').innerHTML = html;
  observeRise();
}

/* $('#filters') et $('#pager') n'existent que sur la page « À table »
   (coquille SPA ou page statique /a-table/) : on protège l'écoute. */
if ($('#filters')) $('#filters').addEventListener('click', e => {
  const b = e.target.closest('.chip');
  if (!b) return;
  state.cat = b.dataset.cat; state.page = 1;
  renderFilters(); renderList();
  window.scrollTo({ top: 240, behavior: 'smooth' });
});

if ($('#pager')) $('#pager').addEventListener('click', e => {
  const b = e.target.closest('.pager__b');
  if (!b || b.disabled) return;
  state.page = Number(b.dataset.page);
  renderList();
  window.scrollTo({ top: 240, behavior: 'smooth' });
});

/* ---------------------------- Article ---------------------------- */
function articleHTML(a) {
  const idx = ARTICLES.indexOf(a);
  const next = ARTICLES[(idx + 1) % ARTICLES.length];

  const recipe = a.type === 'recette' ? `
    <div class="card" style="padding:40px">
      <h2 class="serif" style="font-size:28px">La recette</h2>
      <div class="dotted dotted--pomme" style="max-width:150px;margin:12px 0 30px"></div>
      <p class="card__kicker" style="margin-bottom:16px">CE QU'IL FAUT</p>
      <div class="ing" style="margin-bottom:34px">${a.ing.map(i => `<div>${i}</div>`).join('')}</div>
      <p class="card__kicker" style="margin-bottom:16px">ON Y VA</p>
      <div style="display:flex;flex-direction:column;gap:20px">
        ${a.steps.map((s, i) => `<div class="recipe-step"><div class="recipe-step__n">${i + 1}</div><p class="recipe-step__t">${s}</p></div>`).join('')}
      </div>
    </div>
    <div class="panel--or" style="margin-top:26px">
      <h2 class="serif" style="font-size:24px;margin-bottom:14px">À faire faire aux enfants</h2>
      <p style="font-size:15.5px;line-height:1.7">${a.enfants}</p>
    </div>` : `
    <div class="card" style="padding:40px">
      <h2 class="serif" style="font-size:28px">Les notes</h2>
      <div class="dotted dotted--pomme" style="max-width:150px;margin:12px 0 30px"></div>
      ${a.corps.map(p => `<p class="body" style="margin-bottom:20px">${p}</p>`).join('')}
    </div>`;

  const aside = a.type === 'recette' ? `
    <p class="card__kicker" style="color:var(--encre-55);margin-bottom:14px">L'HISTOIRE QUI VA AVEC</p>
    ${a.recit.map((p, i) => i === 0
      ? `<p class="serif" style="font-size:19px;line-height:1.62;color:rgba(83,71,65,.86);margin-bottom:18px">${p}</p>`
      : `<p class="body" style="font-size:15.5px;margin-bottom:18px">${p}</p>`).join('')}` : `
    <p class="card__kicker" style="color:var(--encre-55);margin-bottom:14px">D'OÙ ÇA VIENT</p>
    <p class="serif" style="font-size:19px;line-height:1.62;color:rgba(83,71,65,.86);margin-bottom:18px">${a.chapeau}</p>`;

  return `
  <a class="back" href="/a-table"><span class="ar">←</span> Retour à table</a>
  <article>
  <div class="article-lead" style="margin-top:34px">
    <p class="eyebrow" style="margin-bottom:18px">${a.source}</p>
    <h1 style="font-size:clamp(34px,4.6vw,54px);margin-bottom:18px">${a.title}</h1>
    <p class="lede" style="margin-bottom:26px">${a.chapeau}</p>
    <div class="article-meta"><span>${a.date}</span>${a.meta.map(m => `<span>${m}</span>`).join('')}</div>
  </div>

  <!-- Suppose qu'un .webp existe à côté de chaque a.img (voir scripts/generate-webp.py) :
       générez-le avant de publier un article avec une nouvelle photo. -->
  <div class="ph ph--r20${a.img ? ' has-img' : ''}" style="height:400px;margin:34px 0 10px">${a.img ? `<picture><source srcset="${a.img.replace(/\.(jpg|jpeg|png)$/i, '.webp')}" type="image/webp"><img src="${a.img}" alt="${a.photo}" width="800" height="400" loading="lazy"></picture>` : `<span>${a.photo}</span>`}</div>

  <div class="row" style="gap:52px;align-items:flex-start;padding-top:44px">
    <div style="flex:1.5;min-width:330px">${recipe}</div>
    <div style="flex:1;min-width:280px">
      <img class="card__ill" src="/images/${a.ill}.svg" alt=""${illAttrs(a.ill)} loading="lazy" style="width:150px;margin-bottom:26px">
      ${aside}
      <div class="quote-mark" style="margin:26px 0">
        <p class="card__kicker card__kicker--green" style="margin-bottom:8px">LA QUESTION À POSER</p>
        <p class="serif" style="font-size:19px;line-height:1.5">${a.question}</p>
      </div>
      <div class="card card--r16" style="padding:24px">
        <p class="card__kicker" style="color:var(--encre-55);margin-bottom:12px">POUR ALLER LIRE</p>
        <div style="font-size:14.5px;line-height:1.7;color:rgba(83,71,65,.78)">
          ${a.lectures.map(l => `<div style="margin-bottom:8px">${l}</div>`).join('')}
        </div>
      </div>
    </div>
  </div>
  </article>

  <div class="panel panel--ink" style="margin:60px 0 30px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:26px;padding:52px">
    <img class="panel__ill" src="/images/livre-cream.svg" alt="" width="112" height="169" loading="lazy" style="right:44px;bottom:-16px;width:150px;opacity:.14">
    <div style="position:relative;max-width:520px">
      <p class="eyebrow eyebrow--or" style="margin-bottom:14px">LA PROCHAINE FOIS</p>
      <p class="serif" style="font-size:28px;line-height:1.35">${next.title} — ${next.resume}</p>
    </div>
    <a class="btn btn--ghost-light" style="position:relative;font-size:15px;padding:13px 26px" href="/a-table/${next.slug}">Lire <span class="ar">→</span></a>
  </div>`;
}

/* Conversion « 12 août 2026 » -> « 2026-08-12 » pour datePublished.
   Utilisée par scripts/generate-article-pages.py (extrait cette fonction
   telle quelle pour poser le JSON-LD BlogPosting de chaque page d'article). */
const MOIS_FR = { janvier: 1, février: 2, mars: 3, avril: 4, mai: 5, juin: 6, juillet: 7, août: 8, septembre: 9, octobre: 10, novembre: 11, décembre: 12 };
function dateFrancaiseVersISO(str) {
  const m = str.match(/(\d+)(?:er)?\s+(\S+)\s+(\d{4})/);
  if (!m) return null;
  const jour = String(m[1]).padStart(2, '0');
  const mois = String(MOIS_FR[m[2].toLowerCase()] || 1).padStart(2, '0');
  return `${m[3]}-${mois}-${jour}`;
}

/* ---------------------------- Apparitions ---------------------------- */
let io;
function observeRise() {
  if (!('IntersectionObserver' in window)) { $$('.rise').forEach(e => e.classList.add('in')); return; }
  io = io || new IntersectionObserver(entries => {
    entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  $$('.rise:not(.in)').forEach(e => io.observe(e));
}

/* ---------------------------- Routage ---------------------------- */
/* index.html est la coquille : elle contient toutes les sections (source de
   generate-static-pages.py) mais n'en affiche qu'une, l'accueil. Chaque
   route a sa vraie page à sa propre URL — /studio, /a-table, /a-table/<slug>,
   etc. Les anciens liens en #/ y sont renvoyés côté client (le serveur ne
   voit jamais le fragment). */
const IS_SPA_SHELL = $$('.page').length > 1;
const MIGRATED_ROUTES = ['studio', 'correction', 'a-table', 'jeu', 'parcours', 'contact'];

function show(page) {
  $$('.page').forEach(s => s.classList.toggle('hide', s.dataset.page !== page));
}

/* Renvoie un ancien lien #/… vers sa vraie URL. true si une redirection
   a été lancée (la requête ?cat=… est conservée). */
function redirectLegacyHash() {
  const raw = (location.hash || '').replace(/^#\/?/, '');
  if (!raw) return false;
  const [path, query] = raw.split('?');
  const parts = path.split('/').filter(Boolean);
  const q = query ? '?' + query : '';
  if (parts[0] === 'ateliers') { location.replace('/studio'); return true; }
  if (parts[0] === 'a-table' && parts[1]) { location.replace('/a-table/' + parts[1] + q); return true; }
  if (parts.length === 1 && MIGRATED_ROUTES.includes(parts[0])) { location.replace('/' + parts[0] + q); return true; }
  return false;
}

/* ---------------------------- Menu mobile ---------------------------- */
const burger = $('#burger');
const navLinks = $('#nav-links');
function closeMenu() {
  document.body.classList.remove('menu-open');
  burger.setAttribute('aria-expanded', 'false');
  burger.setAttribute('aria-label', 'Ouvrir le menu');
}
burger.addEventListener('click', () => {
  const open = !document.body.classList.contains('menu-open');
  document.body.classList.toggle('menu-open', open);
  burger.setAttribute('aria-expanded', String(open));
  burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
});
navLinks.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
window.addEventListener('hashchange', closeMenu);
window.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });

/* ---------------------------- Formulaire ---------------------------- */
/* #form n'existe que sur la page « Contact » (coquille SPA ou page
   statique /contact/) : on protège l'écoute. */
if ($('#form')) $('#form').addEventListener('submit', async e => {
  e.preventDefault();
  const form = e.target;
  const status = $('#form-status');
  const btn = form.querySelector('button[type="submit"]');

  if (!form.checkValidity()) { form.reportValidity(); return; }

  btn.textContent = 'Envoi…';
  btn.disabled = true;
  status.textContent = '';

  try {
    const res = await fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    });
    if (!res.ok) throw new Error('refus du serveur');
    form.reset();
    $('#contact-form').classList.add('hide');
    $('#contact-sent').classList.remove('hide');
    window.scrollTo(0, 0);
  } catch (err) {
    status.textContent = "L'envoi n'a pas abouti. Écrivez-moi directement à bonjour@mythesetmarmites.fr";
    status.style.color = 'var(--pomme)';
  } finally {
    btn.textContent = 'Envoyer';
    btn.disabled = false;
  }
});

/* ---------------------------- Démarrage ---------------------------- */
if (IS_SPA_SHELL) {
  /* Coquille (/). Servie par le repli _redirects pour une URL sans
     fichier ? on renvoie à l'accueil. Sinon on redirige un éventuel
     ancien lien #/… puis on affiche l'accueil. */
  const p = location.pathname.replace(/\/index\.html$/, '').replace(/(.)\/+$/, '$1');
  if (p && p !== '/') {
    location.replace('/');
  } else if (!redirectLegacyHash()) {
    show('accueil');
    window.addEventListener('hashchange', () => { redirectLegacyHash(); });
    observeRise();
  }
} else if ($('#list')) {
  /* Page /a-table/ : la recherche par catégorie passe par ?cat=… */
  const cat = new URLSearchParams(location.search).get('cat');
  if (cat && CATS.some(c => c.id === cat)) state.cat = cat;
  renderFilters();
  renderList();
} else {
  /* Autre page statique : le contenu est déjà en place. */
  observeRise();
}