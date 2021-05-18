from logging import exception
import requests
import datetime
from time import sleep
from fake_useragent import UserAgent

temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}

### Variables

## Important Variables
# 0 = Search entire state, 1 = Search only a single district
method = 1
state_list = {
1 : 'Andaman and Nicobar Islands',
2 : 'Andhra Pradesh',
3 : 'Arunachal Pradesh',
4 : 'Assam',
5 : 'Bihar',
6 : 'Chandigarh',
7 : 'Chhattisgarh',
8 : 'Dadra and Nagar Haveli',
37 : 'Daman and Diu',
9 : 'Delhi',
10 : 'Goa',
11 : 'Gujarat',
12 : 'Haryana',
13 : 'Himachal Pradesh',
14 : 'Jammu and Kashmir',
15 : 'Jharkhand',
16 : 'Karnataka',
17 : 'Kerala',
18 : 'Ladakh',
19 : 'Lakshadweep',
20 : 'Madhya Pradesh',
21 : 'Maharashtra',
22 : 'Manipur',
23 : 'Meghalaya',
24 : 'Mizoram',
25 : 'Nagaland',
26 : 'Odisha',
27 : 'Puducherry',
28 : 'Punjab',
29 : 'Rajasthan',
30 : 'Sikkim',
31 : 'Tamil Nadu',
32 : 'Telangana',
33 : 'Tripura',
34 : 'Uttar Pradesh',
35 : 'Uttarakhand',
36 : 'West Bengal',
}
districts = {
1 : [3, 1, 2, ],
2 : [9, 10, 11, 5, 4, 7, 12, 13, 14, 8, 15, 16, 6, ],
3 : [22, 20, 25, 23, 42, 17, 24, 27, 21, 33, 29, 40, 31, 18, 32, 36, 19, 39, 35, 37, 30, 26, 34, 41, 28, 38, ],
4 : [46, 47, 765, 57, 66, 766, 58, 48, 62, 59, 43, 67, 60, 53, 68, 764, 54, 49, 50, 51, 69, 61, 63, 767, 55, 56, 52, 44, 64, 768, 45, 65, 769, ],
5 : [74, 78, 77, 83, 98, 82, 99, 100, 94, 105, 79, 104, 107, 91, 80, 75, 101, 76, 84, 70, 95, 85, 86, 90, 92, 97, 73, 81, 71, 96, 102, 93, 87, 88, 103, 72, 89, 106, ],
6 : [108, ],
7 : [110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 136, 121, 122, 123, 135, 124, 125, 126, 127, 128, 129, 130, 109, 131, 132, 133, 134, ],
8 : [137, ],
9 : [141, 145, 140, 146, 147, 143, 148, 149, 144, 150, 142, ],
10 : [151, 152, ],
11 : [154, 770, 174, 179, 158, 159, 180, 175, 771, 176, 181, 182, 163, 168, 153, 772, 177, 169, 773, 178, 774, 156, 170, 183, 160, 171, 184, 164, 185, 161, 172, 173, 775, 162, 165, 776, 157, 166, 155, 777, 167, ],
12 : [193, 200, 201, 199, 196, 188, 191, 189, 204, 190, 203, 186, 206, 205, 207, 187, 195, 202, 192, 194, 198, 197, ],
13 : [219, 214, 217, 213, 216, 211, 210, 215, 208, 212, 209, 218, ],
14 : [224, 223, 225, 229, 232, 228, 230, 234, 231, 221, 226, 238, 227, 237, 235, 239, 236, 222, 220, 233, ],
15 : [242, 245, 253, 257, 258, 247, 243, 256, 262, 251, 255, 259, 252, 241, 244, 250, 261, 246, 254, 240, 260, 248, 249, 263, ],
16 : [270, 276, 265, 294, 264, 274, 272, 271, 273, 291, 268, 269, 275, 278, 280, 267, 289, 279, 283, 277, 282, 290, 266, 284, 292, 287, 288, 286, 281, 293, 285, ],
17 : [301, 307, 306, 297, 295, 298, 304, 305, 302, 308, 300, 296, 303, 299, ],
18 : [309, 310, ],
19 : [796, 311, ],
20 : [320, 357, 334, 354, 338, 343, 362, 351, 312, 342, 328, 337, 327, 350, 324, 341, 336, 348, 313, 361, 360, 314, 315, 340, 353, 339, 344, 335, 319, 347, 352, 323, 326, 359, 358, 322, 316, 317, 333, 356, 349, 332, 321, 346, 345, 331, 330, 325, 318, 329, 355, ],
21 : [391, 364, 366, 397, 384, 370, 367, 380, 388, 379, 378, 386, 390, 396, 371, 383, 395, 365, 382, 387, 389, 381, 394, 385, 363, 393, 372, 373, 376, 374, 375, 392, 377, 369, 368, ],
22 : [398, 399, 400, 401, 402, 410, 413, 409, 408, 412, 411, 403, 404, 407, 405, 406, ],
23 : [424, 418, 414, 423, 417, 421, 422, 415, 420, 416, 419, ],
24 : [425, 426, 429, 428, 432, 431, 427, 430, 433, ],
25 : [434, 444, 441, 438, 437, 439, 435, 443, 440, 436, 442, ],
26 : [445, 448, 447, 472, 454, 468, 457, 473, 458, 467, 449, 459, 460, 474, 464, 450, 461, 455, 446, 451, 469, 456, 470, 462, 465, 463, 471, 452, 466, 453, ],
27 : [476, 477, 475, 478, ],
28 : [485, 483, 493, 499, 484, 487, 480, 489, 481, 492, 479, 488, 482, 491, 486, 494, 497, 498, 496, 500, 490, 495, ],
29 : [507, 512, 519, 516, 528, 508, 523, 501, 514, 521, 530, 511, 524, 520, 517, 505, 506, 527, 533, 515, 510, 502, 525, 503, 532, 529, 522, 518, 534, 513, 531, 509, 526, 504, ],
30 : [535, 537, 538, 536, ],
31 : [779, 555, 578, 565, 571, 778, 539, 547, 566, 556, 563, 552, 557, 544, 559, 780, 562, 540, 576, 558, 577, 564, 573, 570, 575, 546, 567, 781, 545, 561, 580, 551, 541, 569, 554, 560, 548, 550, 568, 572, 553, 574, 543, 542, 549, ],
32 : [582, 583, 581, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 612, 597, 598, 613, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, ],
33 : [614, 615, 616, 617, 618, 619, 620, 621, ],
34 : [622, 623, 625, 626, 627, 628, 646, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 687, 639, 640, 641, 642, 643, 644, 645, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 682, 624, 681, 683, 684, 685, 686, 688, 689, 690, 691, 692, 693, 694, 695, 696, ],
35 : [704, 707, 699, 708, 697, 702, 709, 698, 706, 700, 701, 705, 703, ],
36 : [710, 711, 712, 713, 714, 715, 783, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, ],
37 : [138, 139, ],
}
dist_deatails = {
3 : 'Nicobar',
 1 : 'North and Middle Andaman',
 2 : 'South Andaman',
 9 : 'Anantapur',
 10 : 'Chittoor',
 11 : 'East Godavari',
 5 : 'Guntur',
 4 : 'Krishna',
 7 : 'Kurnool',
 12 : 'Prakasam',
 13 : 'Sri Potti Sriramulu Nellore',
 14 : 'Srikakulam',
 8 : 'Visakhapatnam',
 15 : 'Vizianagaram',
 16 : 'West Godavari',
 6 : 'YSR District, Kadapa (Cuddapah)',
 22 : 'Anjaw',
 20 : 'Changlang',
 25 : 'Dibang Valley',
 23 : 'East Kameng',
 42 : 'East Siang',
 17 : 'Itanagar Capital Complex',
 24 : 'Kamle',
 27 : 'Kra Daadi',
 21 : 'Kurung Kumey',
 33 : 'Lepa Rada',
 29 : 'Lohit',
 40 : 'Longding',
 31 : 'Lower Dibang Valley',
 18 : 'Lower Siang',
 32 : 'Lower Subansiri',
 36 : 'Namsai',
 19 : 'Pakke Kessang',
 39 : 'Papum Pare',
 35 : 'Shi Yomi',
 37 : 'Siang',
 30 : 'Tawang',
 26 : 'Tirap',
 34 : 'Upper Siang',
 41 : 'Upper Subansiri',
 28 : 'West Kameng',
 38 : 'West Siang',
 46 : 'Baksa',
 47 : 'Barpeta',
 765 : 'Biswanath',
 57 : 'Bongaigaon',
 66 : 'Cachar',
 766 : 'Charaideo',
 58 : 'Chirang',
 48 : 'Darrang',
 62 : 'Dhemaji',
 59 : 'Dhubri',
 43 : 'Dibrugarh',
 67 : 'Dima Hasao',
 60 : 'Goalpara',
 53 : 'Golaghat',
 68 : 'Hailakandi',
 764 : 'Hojai',
 54 : 'Jorhat',
 49 : 'Kamrup Metropolitan',
 50 : 'Kamrup Rural',
 51 : 'Karbi-Anglong',
 69 : 'Karimganj',
 61 : 'Kokrajhar',
 63 : 'Lakhimpur',
 767 : 'Majuli',
 55 : 'Morigaon',
 56 : 'Nagaon',
 52 : 'Nalbari',
 44 : 'Sivasagar',
 64 : 'Sonitpur',
 768 : 'South Salmara Mankachar',
 45 : 'Tinsukia',
 65 : 'Udalguri',
 769 : 'West Karbi Anglong',
 74 : 'Araria',
 78 : 'Arwal',
 77 : 'Aurangabad',
 83 : 'Banka',
 98 : 'Begusarai',
 82 : 'Bhagalpur',
 99 : 'Bhojpur',
 100 : 'Buxar',
 94 : 'Darbhanga',
 105 : 'East Champaran',
 79 : 'Gaya',
 104 : 'Gopalganj',
 107 : 'Jamui',
 91 : 'Jehanabad',
 80 : 'Kaimur',
 75 : 'Katihar',
 101 : 'Khagaria',
 76 : 'Kishanganj',
 84 : 'Lakhisarai',
 70 : 'Madhepura',
 95 : 'Madhubani',
 85 : 'Munger',
 86 : 'Muzaffarpur',
 90 : 'Nalanda',
 92 : 'Nawada',
 97 : 'Patna',
 73 : 'Purnia',
 81 : 'Rohtas',
 71 : 'Saharsa',
 96 : 'Samastipur',
 102 : 'Saran',
 93 : 'Sheikhpura',
 87 : 'Sheohar',
 88 : 'Sitamarhi',
 103 : 'Siwan',
 72 : 'Supaul',
 89 : 'Vaishali',
 106 : 'West Champaran',
 108 : 'Chandigarh',
 110 : 'Balod',
 111 : 'Baloda bazar',
 112 : 'Balrampur',
 113 : 'Bastar',
 114 : 'Bemetara',
 115 : 'Bijapur',
 116 : 'Bilaspur',
 117 : 'Dantewada',
 118 : 'Dhamtari',
 119 : 'Durg',
 120 : 'Gariaband',
 136 : 'Gaurela Pendra Marwahi ',
 121 : 'Janjgir-Champa',
 122 : 'Jashpur',
 123 : 'Kanker',
 135 : 'Kawardha',
 124 : 'Kondagaon',
 125 : 'Korba',
 126 : 'Koriya',
 127 : 'Mahasamund',
 128 : 'Mungeli',
 129 : 'Narayanpur',
 130 : 'Raigarh',
 109 : 'Raipur',
 131 : 'Rajnandgaon',
 132 : 'Sukma',
 133 : 'Surajpur',
 134 : 'Surguja',
 137 : 'Dadra and Nagar Haveli',
 141 : 'Central Delhi',
 145 : 'East Delhi',
 140 : 'New Delhi',
 146 : 'North Delhi',
 147 : 'North East Delhi',
 143 : 'North West Delhi',
 148 : 'Shahdara',
 149 : 'South Delhi',
 144 : 'South East Delhi',
 150 : 'South West Delhi',
 142 : 'West Delhi',
 151 : 'North Goa',
 152 : 'South Goa',
 154 : 'Ahmedabad',
 770 : 'Ahmedabad Corporation',
 174 : 'Amreli',
 179 : 'Anand',
 158 : 'Aravalli',
 159 : 'Banaskantha',
 180 : 'Bharuch',
 175 : 'Bhavnagar',
 771 : 'Bhavnagar Corporation',
 176 : 'Botad',
 181 : 'Chhotaudepur',
 182 : 'Dahod',
 163 : 'Dang',
 168 : 'Devbhumi Dwaraka',
 153 : 'Gandhinagar',
 772 : 'Gandhinagar Corporation',
 177 : 'Gir Somnath',
 169 : 'Jamnagar',
 773 : 'Jamnagar Corporation',
 178 : 'Junagadh',
 774 : 'Junagadh Corporation',
 156 : 'Kheda',
 170 : 'Kutch',
 183 : 'Mahisagar',
 160 : 'Mehsana',
 171 : 'Morbi',
 184 : 'Narmada',
 164 : 'Navsari',
 185 : 'Panchmahal',
 161 : 'Patan',
 172 : 'Porbandar',
 173 : 'Rajkot',
 775 : 'Rajkot Corporation',
 162 : 'Sabarkantha',
 165 : 'Surat',
 776 : 'Surat Corporation',
 157 : 'Surendranagar',
 166 : 'Tapi',
 155 : 'Vadodara',
 777 : 'Vadodara Corporation',
 167 : 'Valsad',
 193 : 'Ambala',
 200 : 'Bhiwani',
 201 : 'Charkhi Dadri',
 199 : 'Faridabad',
 196 : 'Fatehabad',
 188 : 'Gurgaon',
 191 : 'Hisar',
 189 : 'Jhajjar',
 204 : 'Jind',
 190 : 'Kaithal',
 203 : 'Karnal',
 186 : 'Kurukshetra',
 206 : 'Mahendragarh',
 205 : 'Nuh',
 207 : 'Palwal',
 187 : 'Panchkula',
 195 : 'Panipat',
 202 : 'Rewari',
 192 : 'Rohtak',
 194 : 'Sirsa',
 198 : 'Sonipat',
 197 : 'Yamunanagar',
 219 : 'Bilaspur',
 214 : 'Chamba',
 217 : 'Hamirpur',
 213 : 'Kangra',
 216 : 'Kinnaur',
 211 : 'Kullu',
 210 : 'Lahaul Spiti',
 215 : 'Mandi',
 208 : 'Shimla',
 212 : 'Sirmaur',
 209 : 'Solan',
 218 : 'Una',
 224 : 'Anantnag',
 223 : 'Bandipore',
 225 : 'Baramulla',
 229 : 'Budgam',
 232 : 'Doda',
 228 : 'Ganderbal',
 230 : 'Jammu',
 234 : 'Kathua',
 231 : 'Kishtwar',
 221 : 'Kulgam',
 226 : 'Kupwara',
 238 : 'Poonch',
 227 : 'Pulwama',
 237 : 'Rajouri',
 235 : 'Ramban',
 239 : 'Reasi',
 236 : 'Samba',
 222 : 'Shopian',
 220 : 'Srinagar',
 233 : 'Udhampur',
 242 : 'Bokaro',
 245 : 'Chatra',
 253 : 'Deoghar',
 257 : 'Dhanbad',
 258 : 'Dumka',
 247 : 'East Singhbhum',
 243 : 'Garhwa',
 256 : 'Giridih',
 262 : 'Godda',
 251 : 'Gumla',
 255 : 'Hazaribagh',
 259 : 'Jamtara',
 252 : 'Khunti',
 241 : 'Koderma',
 244 : 'Latehar',
 250 : 'Lohardaga',
 261 : 'Pakur',
 246 : 'Palamu',
 254 : 'Ramgarh',
 240 : 'Ranchi',
 260 : 'Sahebganj',
 248 : 'Seraikela Kharsawan',
 249 : 'Simdega',
 263 : 'West Singhbhum',
 270 : 'Bagalkot',
 276 : 'Bangalore Rural',
 265 : 'Bangalore Urban',
 294 : 'BBMP',
 264 : 'Belgaum',
 274 : 'Bellary',
 272 : 'Bidar',
 271 : 'Chamarajanagar',
 273 : 'Chikamagalur',
 291 : 'Chikkaballapur',
 268 : 'Chitradurga',
 269 : 'Dakshina Kannada',
 275 : 'Davanagere',
 278 : 'Dharwad',
 280 : 'Gadag',
 267 : 'Gulbarga',
 289 : 'Hassan',
 279 : 'Haveri',
 283 : 'Kodagu',
 277 : 'Kolar',
 282 : 'Koppal',
 290 : 'Mandya',
 266 : 'Mysore',
 284 : 'Raichur',
 292 : 'Ramanagara',
 287 : 'Shimoga',
 288 : 'Tumkur',
 286 : 'Udupi',
 281 : 'Uttar Kannada',
 293 : 'Vijayapura',
 285 : 'Yadgir',
 301 : 'Alappuzha',
 307 : 'Ernakulam',
 306 : 'Idukki',
 297 : 'Kannur',
 295 : 'Kasaragod',
 298 : 'Kollam',
 304 : 'Kottayam',
 305 : 'Kozhikode',
 302 : 'Malappuram',
 308 : 'Palakkad',
 300 : 'Pathanamthitta',
 296 : 'Thiruvananthapuram',
 303 : 'Thrissur',
 299 : 'Wayanad',
 309 : 'Kargil',
 310 : 'Leh',
 796 : 'Agatti Island',
 311 : 'Lakshadweep',
 320 : 'Agar',
 357 : 'Alirajpur',
 334 : 'Anuppur',
 354 : 'Ashoknagar',
 338 : 'Balaghat',
 343 : 'Barwani',
 362 : 'Betul',
 351 : 'Bhind',
 312 : 'Bhopal',
 342 : 'Burhanpur',
 328 : 'Chhatarpur',
 337 : 'Chhindwara',
 327 : 'Damoh',
 350 : 'Datia',
 324 : 'Dewas',
 341 : 'Dhar',
 336 : 'Dindori',
 348 : 'Guna',
 313 : 'Gwalior',
 361 : 'Harda',
 360 : 'Hoshangabad',
 314 : 'Indore',
 315 : 'Jabalpur',
 340 : 'Jhabua',
 353 : 'Katni',
 339 : 'Khandwa',
 344 : 'Khargone',
 335 : 'Mandla',
 319 : 'Mandsaur',
 347 : 'Morena',
 352 : 'Narsinghpur',
 323 : 'Neemuch',
 326 : 'Panna',
 359 : 'Raisen',
 358 : 'Rajgarh',
 322 : 'Ratlam',
 316 : 'Rewa',
 317 : 'Sagar',
 333 : 'Satna',
 356 : 'Sehore',
 349 : 'Seoni',
 332 : 'Shahdol',
 321 : 'Shajapur',
 346 : 'Sheopur',
 345 : 'Shivpuri',
 331 : 'Sidhi',
 330 : 'Singrauli',
 325 : 'Tikamgarh',
 318 : 'Ujjain',
 329 : 'Umaria',
 355 : 'Vidisha',
 391 : 'Ahmednagar',
 364 : 'Akola',
 366 : 'Amravati',
 397 : 'Aurangabad ',
 384 : 'Beed',
 370 : 'Bhandara',
 367 : 'Buldhana',
 380 : 'Chandrapur',
 388 : 'Dhule',
 379 : 'Gadchiroli',
 378 : 'Gondia',
 386 : 'Hingoli',
 390 : 'Jalgaon',
 396 : 'Jalna',
 371 : 'Kolhapur',
 383 : 'Latur',
 395 : 'Mumbai',
 365 : 'Nagpur',
 382 : 'Nanded',
 387 : 'Nandurbar',
 389 : 'Nashik',
 381 : 'Osmanabad',
 394 : 'Palghar',
 385 : 'Parbhani',
 363 : 'Pune',
 393 : 'Raigad',
 372 : 'Ratnagiri',
 373 : 'Sangli',
 376 : 'Satara',
 374 : 'Sindhudurg',
 375 : 'Solapur',
 392 : 'Thane',
 377 : 'Wardha',
 369 : 'Washim',
 368 : 'Yavatmal',
 398 : 'Bishnupur',
 399 : 'Chandel',
 400 : 'Churachandpur',
 401 : 'Imphal East',
 402 : 'Imphal West',
 410 : 'Jiribam',
 413 : 'Kakching',
 409 : 'Kamjong',
 408 : 'Kangpokpi',
 412 : 'Noney',
 411 : 'Pherzawl',
 403 : 'Senapati',
 404 : 'Tamenglong',
 407 : 'Tengnoupal',
 405 : 'Thoubal',
 406 : 'Ukhrul',
 424 : 'East Garo Hills',
 418 : 'East Jaintia Hills',
 414 : 'East Khasi Hills',
 423 : 'North Garo Hills',
 417 : 'Ri-Bhoi',
 421 : 'South Garo Hills',
 422 : 'South West Garo Hills',
 415 : 'South West Khasi Hills',
 420 : 'West Garo Hills',
 416 : 'West Jaintia Hills',
 419 : 'West Khasi Hills',
 425 : 'Aizawl East',
 426 : 'Aizawl West',
 429 : 'Champhai',
 428 : 'Kolasib',
 432 : 'Lawngtlai',
 431 : 'Lunglei',
 427 : 'Mamit',
 430 : 'Serchhip',
 433 : 'Siaha',
 434 : 'Dimapur',
 444 : 'Kiphire',
 441 : 'Kohima',
 438 : 'Longleng',
 437 : 'Mokokchung',
 439 : 'Mon',
 435 : 'Peren',
 443 : 'Phek',
 440 : 'Tuensang',
 436 : 'Wokha',
 442 : 'Zunheboto',
 445 : 'Angul',
 448 : 'Balangir',
 447 : 'Balasore',
 472 : 'Bargarh',
 454 : 'Bhadrak',
 468 : 'Boudh',
 457 : 'Cuttack',
 473 : 'Deogarh',
 458 : 'Dhenkanal',
 467 : 'Gajapati',
 449 : 'Ganjam',
 459 : 'Jagatsinghpur',
 460 : 'Jajpur',
 474 : 'Jharsuguda',
 464 : 'Kalahandi',
 450 : 'Kandhamal',
 461 : 'Kendrapara',
 455 : 'Kendujhar',
 446 : 'Khurda',
 451 : 'Koraput',
 469 : 'Malkangiri',
 456 : 'Mayurbhanj',
 470 : 'Nabarangpur',
 462 : 'Nayagarh',
 465 : 'Nuapada',
 463 : 'Puri',
 471 : 'Rayagada',
 452 : 'Sambalpur',
 466 : 'Subarnapur',
 453 : 'Sundargarh',
 476 : 'Karaikal',
 477 : 'Mahe',
 475 : 'Puducherry',
 478 : 'Yanam',
 485 : 'Amritsar',
 483 : 'Barnala',
 493 : 'Bathinda',
 499 : 'Faridkot',
 484 : 'Fatehgarh Sahib',
 487 : 'Fazilka',
 480 : 'Ferozpur',
 489 : 'Gurdaspur',
 481 : 'Hoshiarpur',
 492 : 'Jalandhar',
 479 : 'Kapurthala',
 488 : 'Ludhiana',
 482 : 'Mansa',
 491 : 'Moga',
 486 : 'Pathankot',
 494 : 'Patiala',
 497 : 'Rup Nagar',
 498 : 'Sangrur',
 496 : 'SAS Nagar',
 500 : 'SBS Nagar',
 490 : 'Sri Muktsar Sahib',
 495 : 'Tarn Taran',
 507 : 'Ajmer',
 512 : 'Alwar',
 519 : 'Banswara',
 516 : 'Baran',
 528 : 'Barmer',
 508 : 'Bharatpur',
 523 : 'Bhilwara',
 501 : 'Bikaner',
 514 : 'Bundi',
 521 : 'Chittorgarh',
 530 : 'Churu',
 511 : 'Dausa',
 524 : 'Dholpur',
 520 : 'Dungarpur',
 517 : 'Hanumangarh',
 505 : 'Jaipur I',
 506 : 'Jaipur II',
 527 : 'Jaisalmer',
 533 : 'Jalore',
 515 : 'Jhalawar',
 510 : 'Jhunjhunu',
 502 : 'Jodhpur',
 525 : 'Karauli',
 503 : 'Kota',
 532 : 'Nagaur',
 529 : 'Pali',
 522 : 'Pratapgarh',
 518 : 'Rajsamand',
 534 : 'Sawai Madhopur',
 513 : 'Sikar',
 531 : 'Sirohi',
 509 : 'Sri Ganganagar',
 526 : 'Tonk',
 504 : 'Udaipur',
 535 : 'East Sikkim',
 537 : 'North Sikkim',
 538 : 'South Sikkim',
 536 : 'West Sikkim',
 779 : 'Aranthangi',
 555 : 'Ariyalur',
 578 : 'Attur',
 565 : 'Chengalpet',
 571 : 'Chennai',
 778 : 'Cheyyar',
 539 : 'Coimbatore',
 547 : 'Cuddalore',
 566 : 'Dharmapuri',
 556 : 'Dindigul',
 563 : 'Erode',
 552 : 'Kallakurichi',
 557 : 'Kanchipuram',
 544 : 'Kanyakumari',
 559 : 'Karur',
 780 : 'Kovilpatti',
 562 : 'Krishnagiri',
 540 : 'Madurai',
 576 : 'Nagapattinam',
 558 : 'Namakkal',
 577 : 'Nilgiris',
 564 : 'Palani',
 573 : 'Paramakudi',
 570 : 'Perambalur',
 575 : 'Poonamallee',
 546 : 'Pudukkottai',
 567 : 'Ramanathapuram',
 781 : 'Ranipet',
 545 : 'Salem',
 561 : 'Sivaganga',
 580 : 'Sivakasi',
 551 : 'Tenkasi',
 541 : 'Thanjavur',
 569 : 'Theni',
 554 : 'Thoothukudi (Tuticorin)',
 560 : 'Tiruchirappalli',
 548 : 'Tirunelveli',
 550 : 'Tirupattur',
 568 : 'Tiruppur',
 572 : 'Tiruvallur',
 553 : 'Tiruvannamalai',
 574 : 'Tiruvarur',
 543 : 'Vellore',
 542 : 'Viluppuram',
 549 : 'Virudhunagar',
 582 : 'Adilabad',
 583 : 'Bhadradri Kothagudem',
 581 : 'Hyderabad',
 584 : 'Jagtial',
 585 : 'Jangaon',
 586 : 'Jayashankar Bhupalpally',
 587 : 'Jogulamba Gadwal',
 588 : 'Kamareddy',
 589 : 'Karimnagar',
 590 : 'Khammam',
 591 : 'Kumuram Bheem',
 592 : 'Mahabubabad',
 593 : 'Mahabubnagar',
 594 : 'Mancherial',
 595 : 'Medak',
 596 : 'Medchal',
 612 : 'Mulugu',
 597 : 'Nagarkurnool',
 598 : 'Nalgonda',
 613 : 'Narayanpet',
 599 : 'Nirmal',
 600 : 'Nizamabad',
 601 : 'Peddapalli',
 602 : 'Rajanna Sircilla',
 603 : 'Rangareddy',
 604 : 'Sangareddy',
 605 : 'Siddipet',
 606 : 'Suryapet',
 607 : 'Vikarabad',
 608 : 'Wanaparthy',
 609 : 'Warangal(Rural)',
 610 : 'Warangal(Urban)',
 611 : 'Yadadri Bhuvanagiri',
 614 : 'Dhalai',
 615 : 'Gomati',
 616 : 'Khowai',
 617 : 'North Tripura',
 618 : 'Sepahijala',
 619 : 'South Tripura',
 620 : 'Unakoti',
 621 : 'West Tripura',
 622 : 'Agra',
 623 : 'Aligarh',
 625 : 'Ambedkar Nagar',
 626 : 'Amethi',
 627 : 'Amroha',
 628 : 'Auraiya',
 646 : 'Ayodhya',
 629 : 'Azamgarh',
 630 : 'Badaun',
 631 : 'Baghpat',
 632 : 'Bahraich',
 633 : 'Balarampur',
 634 : 'Ballia',
 635 : 'Banda',
 636 : 'Barabanki',
 637 : 'Bareilly',
 638 : 'Basti',
 687 : 'Bhadohi',
 639 : 'Bijnour',
 640 : 'Bulandshahr',
 641 : 'Chandauli',
 642 : 'Chitrakoot',
 643 : 'Deoria',
 644 : 'Etah',
 645 : 'Etawah',
 647 : 'Farrukhabad',
 648 : 'Fatehpur',
 649 : 'Firozabad',
 650 : 'Gautam Buddha Nagar',
 651 : 'Ghaziabad',
 652 : 'Ghazipur',
 653 : 'Gonda',
 654 : 'Gorakhpur',
 655 : 'Hamirpur',
 656 : 'Hapur',
 657 : 'Hardoi',
 658 : 'Hathras',
 659 : 'Jalaun',
 660 : 'Jaunpur',
 661 : 'Jhansi',
 662 : 'Kannauj',
 663 : 'Kanpur Dehat',
 664 : 'Kanpur Nagar',
 665 : 'Kasganj',
 666 : 'Kaushambi',
 667 : 'Kushinagar',
 668 : 'Lakhimpur Kheri',
 669 : 'Lalitpur',
 670 : 'Lucknow',
 671 : 'Maharajganj',
 672 : 'Mahoba',
 673 : 'Mainpuri',
 674 : 'Mathura',
 675 : 'Mau',
 676 : 'Meerut',
 677 : 'Mirzapur',
 678 : 'Moradabad',
 679 : 'Muzaffarnagar',
 680 : 'Pilibhit',
 682 : 'Pratapgarh',
 624 : 'Prayagraj',
 681 : 'Raebareli',
 683 : 'Rampur',
 684 : 'Saharanpur',
 685 : 'Sambhal',
 686 : 'Sant Kabir Nagar',
 688 : 'Shahjahanpur',
 689 : 'Shamli',
 690 : 'Shravasti',
 691 : 'Siddharthnagar',
 692 : 'Sitapur',
 693 : 'Sonbhadra',
 694 : 'Sultanpur',
 695 : 'Unnao',
 696 : 'Varanasi',
 704 : 'Almora',
 707 : 'Bageshwar',
 699 : 'Chamoli',
 708 : 'Champawat',
 697 : 'Dehradun',
 702 : 'Haridwar',
 709 : 'Nainital',
 698 : 'Pauri Garhwal',
 706 : 'Pithoragarh',
 700 : 'Rudraprayag',
 701 : 'Tehri Garhwal',
 705 : 'Udham Singh Nagar',
 703 : 'Uttarkashi',
 710 : 'Alipurduar District',
 711 : 'Bankura',
 712 : 'Basirhat HD (North 24 Parganas)',
 713 : 'Birbhum',
 714 : 'Bishnupur HD (Bankura)',
 715 : 'Cooch Behar',
 783 : 'COOCHBEHAR',
 716 : 'Dakshin Dinajpur',
 717 : 'Darjeeling',
 718 : 'Diamond Harbor HD (S 24 Parganas)',
 719 : 'East Bardhaman',
 720 : 'Hoogly',
 721 : 'Howrah',
 722 : 'Jalpaiguri',
 723 : 'Jhargram',
 724 : 'Kalimpong',
 725 : 'Kolkata',
 726 : 'Malda',
 727 : 'Murshidabad',
 728 : 'Nadia',
 729 : 'Nandigram HD (East Medinipore)',
 730 : 'North 24 Parganas',
 731 : 'Paschim Medinipore',
 732 : 'Purba Medinipore',
 733 : 'Purulia',
 734 : 'Rampurhat HD (Birbhum)',
 735 : 'South 24 Parganas',
 736 : 'Uttar Dinajpur',
 737 : 'West Bardhaman',
 138 : 'Daman',
 139 : 'Diu',
}
vaccineshot = ""
def showDistricts():
    scode = int(input("Enter your state code: "))
    if scode in districts.keys():
        dcodes = districts[scode]
        for i in dcodes:
            print(f"{i} -> {dist_deatails[i]}\n")
    else:
        print("Invalid input...")


def showStates():
    for i in state_list.keys():
        print(f"{i} -> {state_list[i]}\n")


# Set state code or district code 0 to query state and district code list
print("Welcome to Cowin Slot checking software.\nFirst check your state and district's code before continuing to software.\n**If you already know your codes please press 3 to continue.\n")
while True:
    a = int(input("************* Please Select Appropriate aption to proceed****************\n1. Enter 1 to see all state codes\n2. Enter 2 to see District list\n3. Enter 3 to continue\n"))
    if a== 1:
        showStates()
    elif a==2:
        showDistricts()
    elif a==3:
        state_code = int(input("Enter state code: "))
        district_code = int(input("Enter Dist code: "))
        if state_code in districts.keys() and district_code in districts[state_code]:
            b= int(input("****Dose Details****\n1. Enter 1 for first dose avilability \n2. Enter 2 for 2nd Dose avilability\n --->"))
            if b == 1:
                vaccineshot = "available_capacity_dose1"
            elif b == 2:
                vaccineshot = "available_capacity_dose2"
            else:
                print("invalid input. Please try again...")
                continue
            break
        else:
            print("Inavalid codes please try agin.")
            continue
    else:
        print("Invalid Input")
                   

# Set your age
age = int(input("Enter your age: "))


## Optional Variables
# Print extra information? (like slots not avaialble on XX-XX-XXXX) (0=No and 1=Yes)
print_detailed = 0

# Number of days to check in advance
numdays = 4

# Check variables
def ageCalculator(age):
    if age<45 and age>=18:
        return 18
    if age>45:
        return 45
    else:
        return 0    

### Script
# Find today's date
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]
# print(date_str)
def checkDistrict(DIST_ID):
    global print_detailed
    global age
    none_found = 1
    for INP_DATE in date_str:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
        response = requests.get(URL,  headers=browser_header)
        if response.ok:
            slots_age = 0
            resp_json = response.json()
            if resp_json["centers"]:
                    for center in resp_json["centers"]:
                        for session in center["sessions"]:
                            if (session["min_age_limit"] == ageCalculator(age)) and (session[f"{vaccineshot}"] > 0):
                                slots_age=1
                                none_found=0
                                print()
                                print("\t", INP_DATE)
                                print("\t", center["name"])
                                print("\t Pincode:", center["pincode"])
                                print("\t Available Capacity: ", session[f"{vaccineshot}"])
                                if(session["vaccine"] != ''):
                                    print("\t Vaccine: ", session["vaccine"])
                                print("\t Fees: ", center["fee_type"])
                                with open(f"log_of_age-{age}.log","a") as f:
                                    f.write(f"""{datetime.datetime.now()}    Date-{INP_DATE} Center- {center["name"]} Slots - {session[f"{vaccineshot}"]} {vaccineshot} {session["vaccine"]}\n""")

        else:
            print("Respose is not getting through")
        if print_detailed==1:
            if slots_age==0:
                print("\tNo available slots on {} for your age".format(INP_DATE))

    if none_found==1:
        print("\t-\tNONE.")


# Execute
while True:
    if method==1:
        checkDistrict(district_code)

    print(f"\nSEARCH COMPLETE. at {datetime.datetime.now()} ")
    sleep(20)
