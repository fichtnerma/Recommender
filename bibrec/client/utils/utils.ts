export function getTimezoneCountry() {
	const countriesMap = new Map([
		["AD", "Andorra"],
		["AE", "United Arab Emirates"],
		["AF", "Afghanistan"],
		["AG", "Antigua and Barbuda"],
		["AI", "Anguilla"],
		["AL", "Albania"],
		["AM", "Armenia"],
		["AO", "Angola"],
		["AQ", "Antarctica"],
		["AR", "Argentina"],
		["AS", "American Samoa"],
		["AT", "Austria"],
		["AU", "Australia"],
		["AW", "Aruba"],
		["AX", "Åland Islands"],
		["AZ", "Azerbaijan"],
		["BA", "Bosnia and Herzegovina"],
		["BB", "Barbados"],
		["BD", "Bangladesh"],
		["BE", "Belgium"],
		["BF", "Burkina Faso"],
		["BG", "Bulgaria"],
		["BH", "Bahrain"],
		["BI", "Burundi"],
		["BJ", "Benin"],
		["BL", "Saint Barthélemy"],
		["BM", "Bermuda"],
		["BN", "Brunei"],
		["BO", "Bolivia"],
		["BQ", "Caribbean Netherlands"],
		["BR", "Brazil"],
		["BS", "Bahamas"],
		["BT", "Bhutan"],
		["BV", "Bouvet Island"],
		["BW", "Botswana"],
		["BY", "Belarus"],
		["BZ", "Belize"],
		["CA", "Canada"],
		["CC", "Cocos Islands"],
		["CD", "Democratic Republic of the Congo"],
		["CF", "Central African Republic"],
		["CG", "Republic of the Congo"],
		["CH", "Switzerland"],
		["CI", "Ivory Coast"],
		["CK", "Cook Islands"],
		["CL", "Chile"],
		["CM", "Cameroon"],
		["CN", "China"],
		["CO", "Colombia"],
		["CR", "Costa Rica"],
		["CU", "Cuba"],
		["CV", "Cabo Verde"],
		["CW", "Curaçao"],
		["CX", "Christmas Island"],
		["CY", "Cyprus"],
		["CZ", "Czechia"],
		["DE", "Germany"],
		["DJ", "Djibouti"],
		["DK", "Denmark"],
		["DM", "Dominica"],
		["DO", "Dominican Republic"],
		["DZ", "Algeria"],
		["EC", "Ecuador"],
		["EE", "Estonia"],
		["EG", "Egypt"],
		["EH", "Western Sahara"],
		["ER", "Eritrea"],
		["ES", "Spain"],
		["ET", "Ethiopia"],
		["FI", "Finland"],
		["FJ", "Fiji"],
		["FK", "Falkland Islands"],
		["FM", "Micronesia"],
		["FO", "Faroe Islands"],
		["FR", "France"],
		["GA", "Gabon"],
		["GB", "United Kingdom"],
		["GD", "Grenada"],
		["GE", "Georgia"],
		["GF", "French Guiana"],
		["GG", "Guernsey"],
		["GH", "Ghana"],
		["GI", "Gibraltar"],
		["GL", "Greenland"],
		["GM", "Gambia"],
		["GN", "Guinea"],
		["GP", "Guadeloupe"],
		["GQ", "Equatorial Guinea"],
		["GR", "Greece"],
		["GS", "South Georgia and the South Sandwich Islands"],
		["GT", "Guatemala"],
		["GU", "Guam"],
		["GW", "Guinea-Bissau"],
		["GY", "Guyana"],
		["HK", "Hong Kong"],
		["HM", "Heard Island and McDonald Islands"],
		["HN", "Honduras"],
		["HR", "Croatia"],
		["HT", "Haiti"],
		["HU", "Hungary"],
		["ID", "Indonesia"],
		["IE", "Ireland"],
		["IL", "Israel"],
		["IM", "Isle of Man"],
		["IN", "India"],
		["IO", "British Indian Ocean Territory"],
		["IQ", "Iraq"],
		["IR", "Iran"],
		["IS", "Iceland"],
		["IT", "Italy"],
		["JE", "Jersey"],
		["JM", "Jamaica"],
		["JO", "Jordan"],
		["JP", "Japan"],
		["KE", "Kenya"],
		["KG", "Kyrgyzstan"],
		["KH", "Cambodia"],
		["KI", "Kiribati"],
		["KM", "Comoros"],
		["KN", "Saint Kitts and Nevis"],
		["KP", "North Korea"],
		["KR", "South Korea"],
		["KW", "Kuwait"],
		["KY", "Cayman Islands"],
		["KZ", "Kazakhstan"],
		["LA", "Laos"],
		["LB", "Lebanon"],
		["LC", "Saint Lucia"],
		["LI", "Liechtenstein"],
		["LK", "Sri Lanka"],
		["LR", "Liberia"],
		["LS", "Lesotho"],
		["LT", "Lithuania"],
		["LU", "Luxembourg"],
		["LV", "Latvia"],
		["LY", "Libya"],
		["MA", "Morocco"],
		["MC", "Monaco"],
		["MD", "Moldova"],
		["ME", "Montenegro"],
		["MF", "Saint Martin"],
		["MG", "Madagascar"],
		["MH", "Marshall Islands"],
		["MK", "North Macedonia"],
		["ML", "Mali"],
		["MM", "Myanmar"],
		["MN", "Mongolia"],
		["MO", "Macao"],
		["MP", "Northern Mariana Islands"],
		["MQ", "Martinique"],
		["MR", "Mauritania"],
		["MS", "Montserrat"],
		["MT", "Malta"],
		["MU", "Mauritius"],
		["MV", "Maldives"],
		["MW", "Malawi"],
		["MX", "Mexico"],
		["MY", "Malaysia"],
		["MZ", "Mozambique"],
		["NA", "Namibia"],
		["NC", "New Caledonia"],
		["NE", "Niger"],
		["NF", "Norfolk Island"],
		["NG", "Nigeria"],
		["NI", "Nicaragua"],
		["NL", "Netherlands"],
		["NO", "Norway"],
		["NP", "Nepal"],
		["NR", "Nauru"],
		["NU", "Niue"],
		["NZ", "New Zealand"],
		["OM", "Oman"],
		["PA", "Panama"],
		["PE", "Peru"],
		["PF", "French Polynesia"],
		["PG", "Papua New Guinea"],
		["PH", "Philippines"],
		["PK", "Pakistan"],
		["PL", "Poland"],
		["PM", "Saint Pierre and Miquelon"],
		["PN", "Pitcairn"],
		["PR", "Puerto Rico"],
		["PS", "Palestine"],
		["PT", "Portugal"],
		["PW", "Palau"],
		["PY", "Paraguay"],
		["QA", "Qatar"],
		["RE", "Réunion"],
		["RO", "Romania"],
		["RS", "Serbia"],
		["RU", "Russia"],
		["RW", "Rwanda"],
		["SA", "Saudi Arabia"],
		["SB", "Solomon Islands"],
		["SC", "Seychelles"],
		["SD", "Sudan"],
		["SE", "Sweden"],
		["SG", "Singapore"],
		["SH", "Saint Helena, Ascension and Tristan da Cunha"],
		["SI", "Slovenia"],
		["SJ", "Svalbard and Jan Mayen"],
		["SK", "Slovakia"],
		["SL", "Sierra Leone"],
		["SM", "San Marino"],
		["SN", "Senegal"],
		["SO", "Somalia"],
		["SR", "Suriname"],
		["SS", "South Sudan"],
		["ST", "Sao Tome and Principe"],
		["SV", "El Salvador"],
		["SX", "Sint Maarten"],
		["SY", "Syria"],
		["SZ", "Eswatini"],
		["TC", "Turks and Caicos Islands"],
		["TD", "Chad"],
		["TF", "French Southern Territories"],
		["TG", "Togo"],
		["TH", "Thailand"],
		["TJ", "Tajikistan"],
		["TK", "Tokelau"],
		["TL", "Timor-Leste"],
		["TM", "Turkmenistan"],
		["TN", "Tunisia"],
		["TO", "Tonga"],
		["TR", "Turkey"],
		["TT", "Trinidad and Tobago"],
		["TV", "Tuvalu"],
		["TW", "Taiwan"],
		["TZ", "Tanzania"],
		["UA", "Ukraine"],
		["UG", "Uganda"],
		["UM", "United States Minor Outlying Islands"],
		["US", "United States of America"],
		["UY", "Uruguay"],
		["UZ", "Uzbekistan"],
		["VA", "Holy See"],
		["VC", "Saint Vincent and the Grenadines"],
		["VE", "Venezuela"],
		["VG", "Virgin Islands (UK)"],
		["VI", "Virgin Islands (US)"],
		["VN", "Vietnam"],
		["VU", "Vanuatu"],
		["WF", "Wallis and Futuna"],
		["WS", "Samoa"],
		["YE", "Yemen"],
		["YT", "Mayotte"],
		["ZA", "South Africa"],
		["ZM", "Zambia"],
		["ZW", "Zimbabwe"]
	]);

	const timezoneMap = new Map([
		["Africa/Abidjan", ["CI", "BF", "GH", "GM", "GN", "ML", "MR", "SH", "SL", "SN", "TG"]],
		["Africa/Accra", ["GH"]],
		["Africa/Addis_Ababa", ["ET"]],
		["Africa/Algiers", ["DZ"]],
		["Africa/Asmara", ["ER"]],
		["Africa/Asmera", ["ER"]],
		["Africa/Bamako", ["ML"]],
		["Africa/Bangui", ["CF"]],
		["Africa/Banjul", ["GM"]],
		["Africa/Bissau", ["GW"]],
		["Africa/Blantyre", ["MW"]],
		["Africa/Brazzaville", ["CG"]],
		["Africa/Bujumbura", ["BI"]],
		["Africa/Cairo", ["EG"]],
		["Africa/Casablanca", ["MA"]],
		["Africa/Ceuta", ["ES"]],
		["Africa/Conakry", ["GN"]],
		["Africa/Dakar", ["SN"]],
		["Africa/Dar_es_Salaam", ["TZ"]],
		["Africa/Djibouti", ["DJ"]],
		["Africa/Douala", ["CM"]],
		["Africa/El_Aaiun", ["EH"]],
		["Africa/Freetown", ["SL"]],
		["Africa/Gaborone", ["BW"]],
		["Africa/Harare", ["ZW"]],
		["Africa/Johannesburg", ["ZA", "LS", "SZ"]],
		["Africa/Juba", ["SS"]],
		["Africa/Kampala", ["UG"]],
		["Africa/Khartoum", ["SD"]],
		["Africa/Kigali", ["RW"]],
		["Africa/Kinshasa", ["CD"]],
		["Africa/Lagos", ["NG", "AO", "BJ", "CD", "CF", "CG", "CM", "GA", "GQ", "NE"]],
		["Africa/Libreville", ["GA"]],
		["Africa/Lome", ["TG"]],
		["Africa/Luanda", ["AO"]],
		["Africa/Lubumbashi", ["CD"]],
		["Africa/Lusaka", ["ZM"]],
		["Africa/Malabo", ["GQ"]],
		["Africa/Maputo", ["MZ", "BI", "BW", "CD", "MW", "RW", "ZM", "ZW"]],
		["Africa/Maseru", ["LS"]],
		["Africa/Mbabane", ["SZ"]],
		["Africa/Mogadishu", ["SO"]],
		["Africa/Monrovia", ["LR"]],
		["Africa/Nairobi", ["KE", "DJ", "ER", "ET", "KM", "MG", "SO", "TZ", "UG", "YT"]],
		["Africa/Ndjamena", ["TD"]],
		["Africa/Niamey", ["NE"]],
		["Africa/Nouakchott", ["MR"]],
		["Africa/Ouagadougou", ["BF"]],
		["Africa/Porto-Novo", ["BJ"]],
		["Africa/Sao_Tome", ["ST"]],
		["Africa/Timbuktu", ["ML"]],
		["Africa/Tripoli", ["LY"]],
		["Africa/Tunis", ["TN"]],
		["Africa/Windhoek", ["NA"]],
		["America/Adak", ["US"]],
		["America/Anchorage", ["US"]],
		["America/Anguilla", ["AI"]],
		["America/Antigua", ["AG"]],
		["America/Araguaina", ["BR"]],
		["America/Argentina/Buenos_Aires", ["AR"]],
		["America/Argentina/Catamarca", ["AR"]],
		["America/Argentina/Cordoba", ["AR"]],
		["America/Argentina/Jujuy", ["AR"]],
		["America/Argentina/La_Rioja", ["AR"]],
		["America/Argentina/Mendoza", ["AR"]],
		["America/Argentina/Rio_Gallegos", ["AR"]],
		["America/Argentina/Salta", ["AR"]],
		["America/Argentina/San_Juan", ["AR"]],
		["America/Argentina/San_Luis", ["AR"]],
		["America/Argentina/Tucuman", ["AR"]],
		["America/Argentina/Ushuaia", ["AR"]],
		["America/Aruba", ["AW"]],
		["America/Asuncion", ["PY"]],
		["America/Atikokan", ["CA"]],
		["America/Bahia", ["BR"]],
		["America/Bahia_Banderas", ["MX"]],
		["America/Barbados", ["BB"]],
		["America/Belem", ["BR"]],
		["America/Belize", ["BZ"]],
		["America/Blanc-Sablon", ["CA"]],
		["America/Boa_Vista", ["BR"]],
		["America/Bogota", ["CO"]],
		["America/Boise", ["US"]],
		["America/Cambridge_Bay", ["CA"]],
		["America/Campo_Grande", ["BR"]],
		["America/Cancun", ["MX"]],
		["America/Caracas", ["VE"]],
		["America/Cayenne", ["GF"]],
		["America/Cayman", ["KY"]],
		["America/Chicago", ["US"]],
		["America/Chihuahua", ["MX"]],
		["America/Coral_Harbour", ["CA"]],
		["America/Costa_Rica", ["CR"]],
		["America/Creston", ["CA"]],
		["America/Cuiaba", ["BR"]],
		["America/Curacao", ["CW"]],
		["America/Danmarkshavn", ["GL"]],
		["America/Dawson", ["CA"]],
		["America/Dawson_Creek", ["CA"]],
		["America/Denver", ["US"]],
		["America/Detroit", ["US"]],
		["America/Dominica", ["DM"]],
		["America/Edmonton", ["CA"]],
		["America/Eirunepe", ["BR"]],
		["America/El_Salvador", ["SV"]],
		["America/Fort_Nelson", ["CA"]],
		["America/Fortaleza", ["BR"]],
		["America/Glace_Bay", ["CA"]],
		["America/Goose_Bay", ["CA"]],
		["America/Grand_Turk", ["TC"]],
		["America/Grenada", ["GD"]],
		["America/Guadeloupe", ["GP"]],
		["America/Guatemala", ["GT"]],
		["America/Guayaquil", ["EC"]],
		["America/Guyana", ["GY"]],
		["America/Halifax", ["CA"]],
		["America/Havana", ["CU"]],
		["America/Hermosillo", ["MX"]],
		["America/Indiana/Indianapolis", ["US"]],
		["America/Indiana/Knox", ["US"]],
		["America/Indiana/Marengo", ["US"]],
		["America/Indiana/Petersburg", ["US"]],
		["America/Indiana/Tell_City", ["US"]],
		["America/Indiana/Vevay", ["US"]],
		["America/Indiana/Vincennes", ["US"]],
		["America/Indiana/Winamac", ["US"]],
		["America/Inuvik", ["CA"]],
		["America/Iqaluit", ["CA"]],
		["America/Jamaica", ["JM"]],
		["America/Juneau", ["US"]],
		["America/Kentucky/Louisville", ["US"]],
		["America/Kentucky/Monticello", ["US"]],
		["America/Kralendijk", ["BQ"]],
		["America/La_Paz", ["BO"]],
		["America/Lima", ["PE"]],
		["America/Los_Angeles", ["US"]],
		["America/Lower_Princes", ["SX"]],
		["America/Maceio", ["BR"]],
		["America/Managua", ["NI"]],
		["America/Manaus", ["BR"]],
		["America/Marigot", ["MF"]],
		["America/Martinique", ["MQ"]],
		["America/Matamoros", ["MX"]],
		["America/Mazatlan", ["MX"]],
		["America/Menominee", ["US"]],
		["America/Merida", ["MX"]],
		["America/Metlakatla", ["US"]],
		["America/Mexico_City", ["MX"]],
		["America/Miquelon", ["PM"]],
		["America/Moncton", ["CA"]],
		["America/Monterrey", ["MX"]],
		["America/Montevideo", ["UY"]],
		["America/Montreal", ["CA"]],
		["America/Montserrat", ["MS"]],
		["America/Nassau", ["BS"]],
		["America/New_York", ["US"]],
		["America/Nipigon", ["CA"]],
		["America/Nome", ["US"]],
		["America/Noronha", ["BR"]],
		["America/North_Dakota/Beulah", ["US"]],
		["America/North_Dakota/Center", ["US"]],
		["America/North_Dakota/New_Salem", ["US"]],
		["America/Nuuk", ["GL"]],
		["America/Ojinaga", ["MX"]],
		["America/Panama", ["PA", "CA", "KY"]],
		["America/Pangnirtung", ["CA"]],
		["America/Paramaribo", ["SR"]],
		["America/Phoenix", ["US", "CA"]],
		["America/Port-au-Prince", ["HT"]],
		["America/Port_of_Spain", ["TT"]],
		["America/Porto_Velho", ["BR"]],
		["America/Puerto_Rico", ["P", "G", "CA", "AI", "AW", "BL", "BQ", "CW", "DM", "GD", "GP", "KN", "LC", "MF", "MS", "SX", "TT", "VC", "VG", "VI"]],
		["America/Punta_Arenas", ["CL"]],
		["America/Rainy_River", ["CA"]],
		["America/Rankin_Inlet", ["CA"]],
		["America/Recife", ["BR"]],
		["America/Regina", ["CA"]],
		["America/Resolute", ["CA"]],
		["America/Rio_Branco", ["BR"]],
		["America/Santarem", ["BR"]],
		["America/Santiago", ["CL"]],
		["America/Santo_Domingo", ["DO"]],
		["America/Sao_Paulo", ["BR"]],
		["America/Scoresbysund", ["GL"]],
		["America/Sitka", ["US"]],
		["America/St_Barthelemy", ["BL"]],
		["America/St_Johns", ["CA"]],
		["America/St_Kitts", ["KN"]],
		["America/St_Lucia", ["LC"]],
		["America/St_Thomas", ["VI"]],
		["America/St_Vincent", ["VC"]],
		["America/Swift_Current", ["CA"]],
		["America/Tegucigalpa", ["HN"]],
		["America/Thule", ["GL"]],
		["America/Thunder_Bay", ["CA"]],
		["America/Tijuana", ["MX"]],
		["America/Toronto", ["CA", "BS"]],
		["America/Tortola", ["VG"]],
		["America/Vancouver", ["CA"]],
		["America/Virgin", ["VI"]],
		["America/Whitehorse", ["CA"]],
		["America/Winnipeg", ["CA"]],
		["America/Yakutat", ["US"]],
		["America/Yellowknife", ["CA"]],
		["Antarctica/Casey", ["AQ"]],
		["Antarctica/Davis", ["AQ"]],
		["Antarctica/DumontDUrville", ["AQ"]],
		["Antarctica/Macquarie", ["AU"]],
		["Antarctica/Mawson", ["AQ"]],
		["Antarctica/McMurdo", ["AQ"]],
		["Antarctica/Palmer", ["AQ"]],
		["Antarctica/Rothera", ["AQ"]],
		["Antarctica/South_Pole", ["AQ"]],
		["Antarctica/Syowa", ["AQ"]],
		["Antarctica/Troll", ["AQ"]],
		["Antarctica/Vostok", ["AQ"]],
		["Arctic/Longyearbyen", ["SJ"]],
		["Asia/Aden", ["YE"]],
		["Asia/Almaty", ["KZ"]],
		["Asia/Amman", ["JO"]],
		["Asia/Anadyr", ["RU"]],
		["Asia/Aqtau", ["KZ"]],
		["Asia/Aqtobe", ["KZ"]],
		["Asia/Ashgabat", ["TM"]],
		["Asia/Atyrau", ["KZ"]],
		["Asia/Baghdad", ["IQ"]],
		["Asia/Bahrain", ["BH"]],
		["Asia/Baku", ["AZ"]],
		["Asia/Bangkok", ["TH", "KH", "LA", "VN"]],
		["Asia/Barnaul", ["RU"]],
		["Asia/Beirut", ["LB"]],
		["Asia/Bishkek", ["KG"]],
		["Asia/Brunei", ["BN"]],
		["Asia/Chita", ["RU"]],
		["Asia/Choibalsan", ["MN"]],
		["Asia/Colombo", ["LK"]],
		["Asia/Damascus", ["SY"]],
		["Asia/Dhaka", ["BD"]],
		["Asia/Dili", ["TL"]],
		["Asia/Dubai", ["AE", "OM"]],
		["Asia/Dushanbe", ["TJ"]],
		["Asia/Famagusta", ["CY"]],
		["Asia/Gaza", ["PS"]],
		["Asia/Hebron", ["PS"]],
		["Asia/Ho_Chi_Minh", ["VN"]],
		["Asia/Hong_Kong", ["HK"]],
		["Asia/Hovd", ["MN"]],
		["Asia/Irkutsk", ["RU"]],
		["Asia/Jakarta", ["ID"]],
		["Asia/Jayapura", ["ID"]],
		["Asia/Jerusalem", ["IL"]],
		["Asia/Kabul", ["AF"]],
		["Asia/Kamchatka", ["RU"]],
		["Asia/Karachi", ["PK"]],
		["Asia/Kathmandu", ["NP"]],
		["Asia/Khandyga", ["RU"]],
		["Asia/Kolkata", ["IN"]],
		["Asia/Krasnoyarsk", ["RU"]],
		["Asia/Kuala_Lumpur", ["MY"]],
		["Asia/Kuching", ["MY"]],
		["Asia/Kuwait", ["KW"]],
		["Asia/Macau", ["MO"]],
		["Asia/Magadan", ["RU"]],
		["Asia/Makassar", ["ID"]],
		["Asia/Manila", ["PH"]],
		["Asia/Muscat", ["OM"]],
		["Asia/Nicosia", ["CY"]],
		["Asia/Novokuznetsk", ["RU"]],
		["Asia/Novosibirsk", ["RU"]],
		["Asia/Omsk", ["RU"]],
		["Asia/Oral", ["KZ"]],
		["Asia/Phnom_Penh", ["KH"]],
		["Asia/Pontianak", ["ID"]],
		["Asia/Pyongyang", ["KP"]],
		["Asia/Qatar", ["QA", "BH"]],
		["Asia/Qostanay", ["KZ"]],
		["Asia/Qyzylorda", ["KZ"]],
		["Asia/Riyadh", ["SA", "AQ", "KW", "YE"]],
		["Asia/Sakhalin", ["RU"]],
		["Asia/Samarkand", ["UZ"]],
		["Asia/Seoul", ["KR"]],
		["Asia/Shanghai", ["CN"]],
		["Asia/Singapore", ["SG", "MY"]],
		["Asia/Srednekolymsk", ["RU"]],
		["Asia/Taipei", ["TW"]],
		["Asia/Tashkent", ["UZ"]],
		["Asia/Tbilisi", ["GE"]],
		["Asia/Tehran", ["IR"]],
		["Asia/Thimphu", ["BT"]],
		["Asia/Tokyo", ["JP"]],
		["Asia/Tomsk", ["RU"]],
		["Asia/Ulaanbaatar", ["MN"]],
		["Asia/Urumqi", ["CN"]],
		["Asia/Ust-Nera", ["RU"]],
		["Asia/Vientiane", ["LA"]],
		["Asia/Vladivostok", ["RU"]],
		["Asia/Yakutsk", ["RU"]],
		["Asia/Yangon", ["MM"]],
		["Asia/Yekaterinburg", ["RU"]],
		["Asia/Yerevan", ["AM"]],
		["Atlantic/Azores", ["PT"]],
		["Atlantic/Bermuda", ["BM"]],
		["Atlantic/Canary", ["ES"]],
		["Atlantic/Cape_Verde", ["CV"]],
		["Atlantic/Faroe", ["FO"]],
		["Atlantic/Jan_Mayen", ["SJ"]],
		["Atlantic/Madeira", ["PT"]],
		["Atlantic/Reykjavik", ["IS"]],
		["Atlantic/South_Georgia", ["GS"]],
		["Atlantic/St_Helena", ["SH"]],
		["Atlantic/Stanley", ["FK"]],
		["Australia/Adelaide", ["AU"]],
		["Australia/Brisbane", ["AU"]],
		["Australia/Broken_Hill", ["AU"]],
		["Australia/Darwin", ["AU"]],
		["Australia/Eucla", ["AU"]],
		["Australia/Hobart", ["AU"]],
		["Australia/Lindeman", ["AU"]],
		["Australia/Lord_Howe", ["AU"]],
		["Australia/Melbourne", ["AU"]],
		["Australia/Perth", ["AU"]],
		["Australia/Sydney", ["AU"]],
		["Canada/Eastern", ["CA"]],
		["Europe/Amsterdam", ["NL"]],
		["Europe/Andorra", ["AD"]],
		["Europe/Astrakhan", ["RU"]],
		["Europe/Athens", ["GR"]],
		["Europe/Belfast", ["GB"]],
		["Europe/Belgrade", ["RS", "BA", "HR", "ME", "MK", "SI"]],
		["Europe/Berlin", ["DE"]],
		["Europe/Bratislava", ["SK"]],
		["Europe/Brussels", ["BE"]],
		["Europe/Bucharest", ["RO"]],
		["Europe/Budapest", ["HU"]],
		["Europe/Busingen", ["DE"]],
		["Europe/Chisinau", ["MD"]],
		["Europe/Copenhagen", ["DK"]],
		["Europe/Dublin", ["IE"]],
		["Europe/Gibraltar", ["GI"]],
		["Europe/Guernsey", ["GG"]],
		["Europe/Helsinki", ["FI", "AX"]],
		["Europe/Isle_of_Man", ["IM"]],
		["Europe/Istanbul", ["TR"]],
		["Europe/Jersey", ["JE"]],
		["Europe/Kaliningrad", ["RU"]],
		["Europe/Kiev", ["UA"]],
		["Europe/Kirov", ["RU"]],
		["Europe/Lisbon", ["PT"]],
		["Europe/Ljubljana", ["SI"]],
		["Europe/London", ["GB", "GG", "IM", "JE"]],
		["Europe/Luxembourg", ["LU"]],
		["Europe/Madrid", ["ES"]],
		["Europe/Malta", ["MT"]],
		["Europe/Mariehamn", ["AX"]],
		["Europe/Minsk", ["BY"]],
		["Europe/Monaco", ["MC"]],
		["Europe/Moscow", ["RU"]],
		["Europe/Oslo", ["NO", "SJ", "BV"]],
		["Europe/Paris", ["FR"]],
		["Europe/Podgorica", ["ME"]],
		["Europe/Prague", ["CZ", "SK"]],
		["Europe/Riga", ["LV"]],
		["Europe/Rome", ["IT", "SM", "VA"]],
		["Europe/Samara", ["RU"]],
		["Europe/San_Marino", ["SM"]],
		["Europe/Sarajevo", ["BA"]],
		["Europe/Saratov", ["RU"]],
		["Europe/Simferopol", ["RU", "UA"]],
		["Europe/Skopje", ["MK"]],
		["Europe/Sofia", ["BG"]],
		["Europe/Stockholm", ["SE"]],
		["Europe/Tallinn", ["EE"]],
		["Europe/Tirane", ["AL"]],
		["Europe/Ulyanovsk", ["RU"]],
		["Europe/Uzhgorod", ["UA"]],
		["Europe/Vaduz", ["LI"]],
		["Europe/Vatican", ["VA"]],
		["Europe/Vienna", ["AT"]],
		["Europe/Vilnius", ["LT"]],
		["Europe/Volgograd", ["RU"]],
		["Europe/Warsaw", ["PL"]],
		["Europe/Zagreb", ["HR"]],
		["Europe/Zaporozhye", ["UA"]],
		["Europe/Zurich", ["CH", "DE", "LI"]],
		["GB", ["GB"]],
		["GB-Eire", ["GB"]],
		["Indian/Antananarivo", ["MG"]],
		["Indian/Chagos", ["IO"]],
		["Indian/Christmas", ["CX"]],
		["Indian/Cocos", ["CC"]],
		["Indian/Comoro", ["KM"]],
		["Indian/Kerguelen", ["TF", "HM"]],
		["Indian/Mahe", ["SC"]],
		["Indian/Maldives", ["MV"]],
		["Indian/Mauritius", ["MU"]],
		["Indian/Mayotte", ["YT"]],
		["Indian/Reunion", ["RE", "TF"]],
		["NZ", ["NZ"]],
		["Pacific/Apia", ["WS"]],
		["Pacific/Auckland", ["NZ", "AQ"]],
		["Pacific/Bougainville", ["PG"]],
		["Pacific/Chatham", ["NZ"]],
		["Pacific/Chuuk", ["FM"]],
		["Pacific/Easter", ["CL"]],
		["Pacific/Efate", ["VU"]],
		["Pacific/Fakaofo", ["TK"]],
		["Pacific/Fiji", ["FJ"]],
		["Pacific/Funafuti", ["TV"]],
		["Pacific/Galapagos", ["EC"]],
		["Pacific/Gambier", ["PF"]],
		["Pacific/Guadalcanal", ["SB"]],
		["Pacific/Guam", ["GU", "MP"]],
		["Pacific/Honolulu", ["US", "UM"]],
		["Pacific/Johnston", ["UM"]],
		["Pacific/Kanton", ["KI"]],
		["Pacific/Kiritimati", ["KI"]],
		["Pacific/Kosrae", ["FM"]],
		["Pacific/Kwajalein", ["MH"]],
		["Pacific/Majuro", ["MH"]],
		["Pacific/Marquesas", ["PF"]],
		["Pacific/Midway", ["UM"]],
		["Pacific/Nauru", ["NR"]],
		["Pacific/Niue", ["NU"]],
		["Pacific/Norfolk", ["NF"]],
		["Pacific/Noumea", ["NC"]],
		["Pacific/Pago_Pago", ["AS", "UM"]],
		["Pacific/Palau", ["PW"]],
		["Pacific/Pitcairn", ["PN"]],
		["Pacific/Pohnpei", ["FM"]],
		["Pacific/Port_Moresby", ["PG", "AQ"]],
		["Pacific/Rarotonga", ["CK"]],
		["Pacific/Saipan", ["MP"]],
		["Pacific/Samoa", ["WS"]],
		["Pacific/Tahiti", ["PF"]],
		["Pacific/Tarawa", ["KI"]],
		["Pacific/Tongatapu", ["TO"]],
		["Pacific/Wake", ["UM"]],
		["Pacific/Wallis", ["WF"]],
		["Singapore", ["SG"]],
		["US/Arizona", ["US"]],
		["US/Hawaii", ["US"]],
		["US/Samoa", ["WS"]]
	]);

	const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

	if (timezone === "" || !timezone) {
		return undefined;
	}

	const tzObject = timezoneMap.get(timezone);
	if (!tzObject) return undefined;
	const country = tzObject[0];

	return countriesMap.get(country);
}
