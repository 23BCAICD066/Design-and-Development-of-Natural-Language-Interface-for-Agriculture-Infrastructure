import streamlit as st
import re
import time
import random
from datetime import datetime, timedelta

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Agri Assistant - Farming Chatbot",
    page_icon="🌾",
    layout="centered"
)

# --------------------------------------------------
# STYLING (CLEAN CHAT UI)
# --------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%);
        color: #e6edf3;
    }
    .chat-header {
        text-align: center;
        padding: 20px;
        border-bottom: 2px solid #22c55e;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #1a1f2e 0%, #0e1117 100%);
        border-radius: 10px;
        animation: slideDown 0.5s;
    }
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .chat-header h1 {
        color: #22c55e;
        margin: 0;
        font-size: 2.5em;
    }
    .chat-header p {
        color: #9ca3af;
        margin-top: 10px;
    }
    .stChatMessage {
        border-radius: 12px !important;
        padding: 15px !important;
        margin: 10px 0;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        border-top: 1px solid #1f2937;
        color: #9ca3af;
    }
    .quick-btn-container {
        margin: 20px 0;
        padding: 15px;
        background: #1a1f2e;
        border-radius: 10px;
    }
    .stButton button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 8px;
        margin: 5px;
        transition: transform 0.2s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(34,197,94,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="chat-header">
    <h1>🌾 Agri Assistant</h1>
    <p>Your Complete Agricultural Companion | AI-Powered Farming Solutions</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --------------------------------------------------
# WEATHER FUNCTION
# --------------------------------------------------
def get_weather_data():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 18:
        return "Sunny", 28 + random.randint(-5, 5), 45 + random.randint(-10, 10)
    else:
        return "Clear", 18 + random.randint(-3, 3), 60 + random.randint(-10, 10)

# --------------------------------------------------
# FERTILIZER CALCULATOR
# --------------------------------------------------
def calculate_fertilizer(crop, area_ha):
    crop_needs = {
        "rice": {"N": 120, "P": 60, "K": 60},
        "wheat": {"N": 150, "P": 75, "K": 75},
        "maize": {"N": 180, "P": 90, "K": 90},
        "cotton": {"N": 100, "P": 50, "K": 50}
    }
    
    if crop.lower() not in crop_needs:
        return None
    
    needs = crop_needs[crop.lower()]
    urea = (needs["N"] * area_ha) / 0.46
    dap = (needs["P"] * area_ha) / 0.18
    mop = (needs["K"] * area_ha) / 0.60
    
    return {
        "urea_kg": round(urea, 2),
        "dap_kg": round(dap, 2),
        "mop_kg": round(mop, 2)
    }

# --------------------------------------------------
# MARKET PRICES
# --------------------------------------------------
def get_market_prices(crop):
    prices = {
        "rice": {"min": 1800, "max": 2200, "avg": 2000, "trend": "stable"},
        "wheat": {"min": 2000, "max": 2400, "avg": 2200, "trend": "rising"},
        "maize": {"min": 1600, "max": 2000, "avg": 1800, "trend": "stable"},
        "cotton": {"min": 5500, "max": 6500, "avg": 6000, "trend": "rising"},
        "sugarcane": {"min": 350, "max": 400, "avg": 375, "trend": "stable"}
    }
    return prices.get(crop.lower(), {"min": 1000, "max": 1500, "avg": 1250, "trend": "unknown"})

# --------------------------------------------------
# AGRICULTURE KNOWLEDGE BASE (ALL PARAGRAPH FORMAT)
# --------------------------------------------------
DATA = {
    "responses": [
        {"keywords": ["rice", "paddy", "oryza", "dhan", "chawal"], "response": "🌾 For successful rice cultivation, you need clayey loam or clay soil with a pH range of 5.5 to 6.5 and organic carbon above 0.5 percent. The ideal temperature for rice is between 20 and 35 degrees Celsius, with optimum at 25 to 30 degrees, and it requires annual rainfall of 100 to 200 centimeters with high humidity of 70 to 80 percent. There are three main cultivation methods: transplanting method which is most common using nursery raised for 25-30 days with seed rate of 40-50 kg per hectare, direct seeding method that saves labor using 80-100 kg seed per hectare, and the SRI or System of Rice Intensification method which uses young seedlings of 10-12 days with wider spacing of 25x25 centimeters and alternate wetting and drying, giving yield increase of 30 to 50 percent. For high yielding varieties, you can choose short duration varieties like IR-64 and Pusa Basmati 1121 taking 120-125 days, medium duration like Swarna and MTU-1010 taking 125-135 days, or long duration like BPT-5204 and Mahsuri taking 135-150 days. The main growing season is Kharif from June to November, but you can also grow in Rabi from December to April under irrigation or in summer from April to June using short duration varieties. Critical stages for water management are tillering, panicle initiation, and flowering, and you should maintain 5 centimeters of standing water while using AWD or alternate wetting and drying technique which saves up to 30 percent water. For nutrients, apply basal dose of 40:60:40 NPK at transplanting, first top dressing of 40 kg nitrogen at 25 days, second top dressing of 40 kg nitrogen at 45 days, and add 25 kg per hectare of zinc sulfate if zinc deficiency is observed. Major pests include stem borer controlled by pheromone traps and carbofuran granules, leaf folder controlled by neem oil at 5 ml per liter, and brown plant hopper controlled by draining water and applying pymetrozine. Diseases like blast can be controlled with tebuconazole at 1 ml per liter, bacterial blight with streptocycline plus copper oxychloride, and sheath rot with propiconazole at 1 ml per liter. Expected yield ranges from 25-35 quintals per hectare for traditional varieties, 45-60 quintals for hybrids, and 50-70 quintals for SRI method. The economics per hectare shows input cost of ₹35,000 to ₹45,000, yield value of ₹90,000 to ₹1,50,000, giving net profit of ₹55,000 to ₹1,05,000. Pro tips include using certified seeds from recognized agencies, practicing integrated pest management, installing light traps for pest monitoring, and maintaining proper field leveling for uniform water distribution."},
        
        {"keywords": ["wheat", "gehun", "triticum"], "response": "🌾 For successful wheat farming, the crop requires temperatures between 15 and 25 degrees Celsius during growing season and 25 to 30 degrees during ripening, and it is a cool season Rabi crop that is sensitive to frost at flowering stage. The ideal soil conditions are well-drained loamy soil with pH between 6.0 and 7.5, organic matter of 0.5 to 0.75 percent, and you must avoid waterlogging at all costs. Popular high-yielding varieties include HD-2967 which takes 160-165 days giving 50-55 quintals per hectare, PBW-550 taking 150-155 days with disease resistance, DBW-17 taking 145-150 days with high protein content, and WH-1105 taking 150-155 days with drought tolerance. Sowing time varies by region: North India from October 25 to November 20, Central India from November 1 to 30, and Peninsular India from October 15 to November 15. You should use seed rate of 100-125 kg per hectare with row spacing of 20-22.5 centimeters at depth of 5-6 centimeters using drilling or seed drill method. Irrigation is critical at five stages: CRI or crown root initiation at 20-25 days, late tillering at 40-45 days, flowering stage at 60-65 days, milk stage at 80-85 days, and dough stage at 100-105 days. For nutrients, the recommended dose is 120:60:40 NPK kg per hectare, applying full phosphorus and potassium plus one-third nitrogen as basal, then one-third nitrogen at 30 days as first top dressing, and remaining one-third nitrogen at 60 days as second top dressing, plus zinc sulfate at 25 kg per hectare if needed. Pest management includes termites controlled by chlorpyriphos soil treatment, aphids controlled by imidacloprid at 0.3 ml per liter, and brown wheat mite controlled by fenazaquin at 1.5 ml per liter. Disease control measures include yellow rust using tebuconazole at 1 ml per liter, brown rust using propiconazole at 1 ml per liter, and powdery mildew using sulfur dusting. Expected yield is 45-55 quintals per hectare for irrigated conditions, 20-30 quintals for rainfed, and up to 60-70 quintals under high management. Economics show input cost of ₹30,000 to ₹40,000 per hectare, MSP for 2024 at ₹2,275 per quintal, gross income of ₹1,02,000 to ₹1,59,000, and net profit of ₹62,000 to ₹1,19,000 per hectare. Quality parameters to maintain include protein content of 10-12 percent, moisture below 14 percent, test weight above 76 kg per hectoliter, and hectoliter weight above 78 kg per hectoliter. Advanced tips include laser land leveling which saves 20-25 percent water, zero tillage wheat which reduces cost by ₹5,000 per hectare, using happy seeder for residue management, and foliar spray of 2 percent urea at grain filling stage."},
        
        {"keywords": ["maize", "corn", "makka", "bhutta"], "response": "🌽 For complete maize cultivation, the crop requires temperatures between 21 and 27 degrees Celsius as optimum, needs 500 to 800 millimeters of rainfall, and is sensitive to frost as it is a day neutral plant. Soil requirements include well-drained loamy soil with pH of 6.0 to 7.0, good organic matter of 0.8 to 1 percent, and deep soil profile of 45 to 60 centimeters. Hybrid varieties include Ganga-11 taking 90-100 days yielding 50-55 quintals per hectare, Deccan-109 taking 85-95 days with drought tolerance, Vijay taking 95-105 days as sweet corn variety, HQPM-1 taking 100-110 days as quality protein maize, and baby corn varieties like HM-4 and VL-78. Season planning offers three options: Kharif sowing in June-July with harvest in September-October, Rabi sowing in October-November with harvest in February-March, and Spring sowing in January-February with harvest in May-June. Seed management requires 20-25 kg per hectare for Kharif and 25-30 kg for Rabi, with spacing of 60x20 cm for Kharif and 45x20 cm for Rabi, planting depth of 4-5 centimeters, and seed treatment with thiram plus carbendazim. For nutrients, the recommended dose is 180:60:40 NPK kg per hectare, applying 60:60:40 plus 5 tons of FYM as basal, then 60 kg nitrogen at 25 days as first top dressing, and another 60 kg nitrogen at 50 days as second top dressing, plus micronutrients of zinc sulfate 25 kg per hectare and ferrous sulfate 10 kg per hectare. Critical irrigation stages are germination at 0-10 days, knee height stage at 25-30 days, tasseling at 50-55 days, silking at 55-60 days, and grain filling at 70-80 days. Major pests include stem borer controlled by granules in whorl, shoot fly controlled by seed treatment, aphids controlled by imidacloprid spray, and fall armyworm controlled by emamectin benzoate. Disease control includes downy mildew using metalaxyl seed treatment, rust using propiconazole at 1 ml per liter, and leaf blight using mancozeb at 2.5 grams per liter. Expected yields vary by season: Kharif gives 50-60 quintals per hectare, Rabi gives 60-70 quintals, Spring gives 65-75 quintals, baby corn gives 12,000-15,000 ears per hectare, and sweet corn gives 15,000-18,000 ears per hectare. Economics show input cost of ₹40,000 to ₹50,000 per hectare, grain price of ₹1,800 to ₹2,200 per quintal, gross income of ₹90,000 to ₹1,54,000, and net profit of ₹50,000 to ₹1,04,000 per hectare. Value addition opportunities include baby corn giving ₹25,000-30,000 extra per hectare, sweet corn giving ₹40,000-50,000 extra, and popcorn giving ₹60,000-80,000 extra per hectare. Modern practices include drip irrigation which saves 40 percent water, broad bed furrow system for rainfed areas, intercropping with pulses in 1:1 ratio, and mulching with crop residue."},
        
        {"keywords": ["pest", "insect", "bug", "aphid", "borer", "worm", "caterpillar"], "response": "🐛 For integrated pest management, here are detailed control strategies for major crop pests. Stem borer affecting rice, maize, and sugarcane is identified by deadheart and whitehead symptoms, and you should monitor using pheromone traps at 12 per hectare, taking action when economic threshold level reaches 5 percent deadheart or one egg mass per square meter. Biological control using Trichogramma japonicum at 1.5 lakh per hectare is effective, while chemical control uses Carbofuran 3G at 33 kg per hectare, and cultural practice includes collecting and destroying egg masses. Brown plant hopper in rice causes hopper burn and sooty mold, so monitor using light traps and sweep nets with economic threshold level of 5-10 insects per hill, using biological control with Metarhizium anisopliae or chemical control with Pymetrozine at 0.5 gram per liter, and cultural control involves draining water for 2-3 days. Aphids affecting wheat, mustard, and pulses cause curling and stunted growth, so monitor using yellow sticky traps with economic threshold level of 10-15 percent plant infestation, using biological control with ladybird beetles and Chrysoperla, chemical control with Imidacloprid at 0.3 ml per liter, or organic option using neem oil at 5 ml per liter with soap. Pod borer in chickpea and pigeonpea creates holes in pods, so monitor with pheromone traps as economic threshold level is 1-2 larvae per plant, using biological control with HaNPV at 250 LE per hectare, chemical with Indoxacarb at 1 ml per liter, and cultural practices including early sowing and trap cropping. Whitefly in cotton and vegetables causes yellowing and leaf curl, so monitor with yellow sticky traps at 20 per hectare as economic threshold level is 10-15 adults per leaf, using biological control with Encarsia parasitoid, chemical with Diafenthiuron at 1 ml per liter, and cultural control avoiding excessive nitrogen. For organic pest control, prepare neem-based spray by mixing 5 ml neem oil and 1 ml soap per liter of water and apply early morning. Garlic-chilli spray is made by blending 100 grams each of garlic and chilli in 1 liter water, straining and diluting 1:10. Panchagavya as organic booster requires fermenting 5 kg cow dung, 3 liters cow urine, 2 liters milk, 2 liters curd, and 0.5 liter ghee for 15 days. Follow IPM calendar: before sowing do deep ploughing and clean cultivation, at sowing do seed treatment and plant trap crops, during vegetative stage do regular scouting and use light traps, during reproductive stage use pheromone traps and biological control, and at harvesting remove crop residues. Always follow safety guidelines including waiting period before harvest, rotating pesticides to avoid resistance, using protective gear like mask and gloves, disposing containers properly, and maintaining spray records. Pro IPM tips include monitoring fields twice weekly, maintaining field hygiene, using resistant varieties, practicing crop rotation, and encouraging natural enemies."},
        
        {"keywords": ["disease", "blight", "rust", "mildew", "rot", "wilt", "anthracnose", "spot"], "response": "🦠 For comprehensive disease management, here are detailed control strategies for major crop diseases. Rice blast caused by Pyricularia oryzae shows diamond-shaped lesions on leaves and is favorable under high humidity and cloudy weather, with economic threshold level of 5 percent leaf area infected, so use resistant varieties like IR-64, MTU-1010, and Swarna, chemical control with Tricyclazole at 0.6 gram per liter, organic control with Pseudomonas fluorescens at 5 grams per liter, and cultural practice avoiding excess nitrogen. Bacterial blight in rice shows yellowish stripes and leaf wilting, spreading through irrigation water and wind with economic threshold level of 10 percent leaf damage, so use resistant varieties like Pusa Basmati 1121, chemical control with Streptocycline at 0.25 gram per liter, and cultural practice of removing weed hosts. Wheat rust including stem, leaf, and stripe rust shows pustules on leaves and stem, favorable at 15-25 degrees Celsius with high humidity and economic threshold level of 1 percent rust severity, so use resistant varieties like HD-2967 and PBW-550, chemical control with Propiconazole at 1 ml per liter, and cultural practice of removing barberry bushes. Late blight in potato and tomato shows water-soaked lesions with white growth, favorable under cool wet conditions, so take action at first appearance using resistant variety Kufri Pukhraj, chemical control with Metalaxyl plus Mancozeb at 2 grams per liter, and cultural practices of proper drainage and wider spacing. Powdery mildew affecting grapes, mango, and wheat shows white powdery growth, favorable under dry weather with high humidity and economic threshold level of 10 percent leaf coverage, so use resistant grape variety Sonaka, chemical control with sulfur dusting at 20 kg per hectare, and organic option of milk spray at 1:9 ratio. Downy mildew in maize and grapes shows yellow patches with downy growth, favorable at high humidity and 20-25 degrees Celsius with economic threshold level of 5 percent plant infection, so use resistant maize variety Ganga-11, chemical control with Mancozeb at 2.5 grams per liter, and cultural practice of destroying infected plants. For organic disease management, prepare Bordeaux mixture at 1 percent by mixing 1 kg copper sulfate and 1 kg lime in 100 liters water for blights and downy mildew. Copper oxychloride at 0.3 percent uses 300 grams in 100 liters water for fungal diseases. Pseudomonas fluorescens at 5 grams per liter for seed treatment and soil drench controls wilt diseases. Trichoderma formulations at 5 grams per kg seed for seed treatment or 2.5 kg per hectare for soil application control root diseases. For integrated disease management, preventive measures include using certified disease-free seeds, following crop rotation for 3-4 years, maintaining proper spacing, balanced fertilization, and field sanitation. Curative measures include rogue out infected plants, apply fungicides at early stage, alternate systemic and contact fungicides, and follow recommended waiting period. Use weather-based disease warning systems, do regular field scouting weekly, maintain disease register, and use decision support systems."},
        
        {"keywords": ["fertilizer", "manure", "compost", "nutrient", "npk", "urea", "dap", "potash"], "response": "🧪 For fertilizer management, nitrogen is essential for leaf growth, protein synthesis, and chlorophyll formation, with deficiency causing yellowing and stunted growth while excess causes lodging and pest susceptibility. Sources include urea with 46 percent nitrogen, DAP with 18 percent, CAN with 25 percent, and ammonium sulfate with 21 percent. Phosphorus functions in root development, flowering, and energy transfer, with deficiency showing purple leaves and poor root growth, and sources include DAP with 46 percent P2O5, SSP with 16 percent, and NPK complexes. Potassium functions in disease resistance, water regulation, and enzyme activation, with deficiency causing leaf scorching and weak stems, and sources include MOP with 60 percent K2O, SOP with 50 percent, and potassium nitrate with 44 percent. For secondary nutrients, calcium is needed for cell wall structure and membrane integrity with deficiency causing blossom end rot, so apply lime in acid soils. Magnesium is required for chlorophyll formation with deficiency showing interveinal chlorosis, so apply foliar spray of magnesium sulfate at 1 percent. Sulfur functions in protein synthesis and oil content with deficiency causing yellowing of young leaves, so use sulfur-containing fertilizers for oilseeds. For micronutrients, zinc deficiency causes Khaira disease in rice, so apply zinc sulfate at 25 kg per hectare as soil application or 0.5 percent as foliar spray. Iron deficiency shows interveinal chlorosis, so apply ferrous sulfate at 0.5 percent foliar spray. Boron deficiency causes hollow stem and fruit cracking, so apply borax at 0.2 percent foliar spray at flowering. For organic fertilizers, Farm Yard Manure contains 0.5 percent N, 0.2 percent P, and 0.5 percent K, so apply 10-15 tons per hectare to improve soil structure. Vermicompost contains 1.5-2.5 percent N, 1.0-1.5 percent P, and 1.0-1.5 percent K, so apply 2-5 tons per hectare as it is rich in enzymes and growth hormones. Green manure crops like Dhaincha, Sunhemp, and Cowpea produce 40-50 tons biomass per hectare adding 100-150 kg nitrogen. Bio-fertilizers include Rhizobium for pulses fixing 50-100 kg nitrogen per hectare, Azotobacter for cereals fixing 20-40 kg nitrogen, PSB for solubilizing fixed phosphorus, and KMB for mobilizing potassium. The fertilizer calculation formula is fertilizer required equals nutrient required multiplied by 100 divided by percentage nutrient in fertilizer. For example, if you need 120 kg nitrogen per hectare and use urea with 46 percent nitrogen, you need 261 kg urea. For site-specific nutrient management in rice on one hectare, apply 120 kg nitrogen which requires 261 kg urea, 60 kg phosphorus requiring 130 kg DAP or 375 kg SSP, 60 kg potassium requiring 100 kg MOP, and 25 kg zinc requiring 25 kg zinc sulfate. For wheat on one hectare, apply 150 kg nitrogen requiring 326 kg urea, 75 kg phosphorus requiring 163 kg DAP or 469 kg SSP, and 75 kg potassium requiring 125 kg MOP. Smart fertilizer practices include using neem-coated urea which increases efficiency 10-15 percent, deep placement to reduce volatilization, applying in moist soil, and split application in 2-3 splits. Time of application includes basal before sowing for phosphorus, potassium, and one-third nitrogen, first top dressing at 25-30 days for one-third nitrogen, and second top dressing at 45-60 days for remaining one-third nitrogen."},
        
        {"keywords": ["irrigation", "water", "drip", "sprinkler", "flood"], "response": "💧 For irrigation management, drip irrigation is the most efficient method with 90-95 percent efficiency, saving 40-70 percent water, best for vegetables, fruits, and cotton, with investment of ₹50,000 to ₹1,00,000 per hectare and yield increase of 20-50 percent. Sprinkler system has 70-80 percent efficiency, saving 30-50 percent water, best for cereals, pulses, and oilseeds, with investment of ₹30,000 to ₹50,000 per hectare. Flood irrigation has only 40-50 percent efficiency and high water loss, suitable only for rice. Furrow irrigation has 60-70 percent efficiency, best for row crops with moderate cost. For water management by crop, rice requires maintaining 5cm standing water with alternate wetting and drying or AWD technique. Wheat requires critical stages at CRI, flowering, and grain filling with 4-6 irrigations. Maize requires critical stages at tasseling and silking with 5-7 irrigations. Water conservation techniques include mulching using plastic or organic materials, rainwater harvesting, laser land leveling, and soil moisture sensors. Government schemes like PMKSY or Per Drop More Crop provide subsidy of 50-80 percent for micro-irrigation. For rainwater harvesting, you can create farm ponds, check dams, rooftop harvesting systems, and recharge pits. Drip irrigation benefits include water saving up to 60 percent, fertilizer saving of 30-40 percent, higher yields, reduced weed growth, and ability to irrigate in undulating terrain. Sprinkler irrigation is suitable for sandy soils, undulating land, and areas with limited water supply, providing uniform water distribution and frost protection. When planning irrigation, always consider your soil type, crop water requirements, local climate, and water availability to choose the most suitable method for your farm."},
        
        {"keywords": ["organic", "natural", "chemical free", "bio"], "response": "🌱 For organic farming, the principles include no synthetic chemicals, maintaining soil health, biodiversity conservation, and sustainable practices. For organic inputs preparation, vermicompost requires cow dung and crop residues with Eisenia fetida earthworms, taking 45-60 days to produce compost with NPK of 1.5-2.5 percent. Panchagavya is made from cow products including cow dung, urine, milk, curd, and ghee, and it acts as a growth promoter and disease resistance booster when applied as 3 percent spray. Jeevamrut requires cow dung, urine, jaggery, and pulse flour fermented for 5-7 days and applied as soil drench. Neem-based products include neem cake for soil amendment, neem oil as pest repellent, and neem seed extract as insecticide. Bio-fertilizers include Rhizobium for legumes, Azotobacter for cereals, PSB for phosphorus solubilization, and KMB for potassium mobilization. For organic pest management, use trap crops, botanical extracts, pheromone traps, and natural predators. The certification process requires a conversion period of 2-3 years, documentation, inspection by certifying agency, and following NPOP standards. Market opportunities include premium prices of 20-50 percent higher, export potential, and domestic organic markets. Challenges include lower initial yields which are compensated by premium prices, weed management solved by mulching and intercropping, and pest control through IPM and preventive measures. To start organic farming, first convert your land by growing green manure crops, apply plenty of compost and vermicompost, use bio-fertilizers for nutrient supply, and implement integrated pest management using neem-based products and biological controls."},
        
        {"keywords": ["crop rotation", "rotation", "sequence", "cropping pattern"], "response": "🔄 For scientific crop rotation, the benefits include improving soil fertility, breaking pest cycles, reducing weed pressure, increasing yield stability, and diversifying income. Recommended rotations by region include the rice-wheat system in North India where you grow rice in Kharif followed by wheat in Rabi, then maize in Kharif followed by mustard in Rabi, and then green manure followed by wheat. The cotton-wheat system in Central India involves cotton followed by wheat and fallow, or cotton followed by chickpea followed by mung bean. The maize-potato-wheat system in Eastern India produces three crops in 12 months with high productivity. For vegetable rotation, follow leafy vegetables with fruiting vegetables, then root vegetables, then legumes, for example spinach followed by tomato followed by carrot followed by beans. The principles to follow include alternating deep-rooted and shallow-rooted crops, following legumes with cereals, avoiding same family crops consecutively, including green manure crops, and adding cover crops in fallow periods. Family groups for rotation include grasses like rice, wheat, and maize; legumes like pulses, groundnut, and soybean; brassicas like mustard, cabbage, and cauliflower; solanaceous like tomato, brinjal, and chilli; and cucurbits like cucumber, pumpkin, and melons. A 4-year rotation plan could be legume followed by cereal in year one, root crop followed by leafy vegetable in year two, cereal followed by legume in year three, and green manure followed by cash crop in year four. Cover crops for soil health include cowpea, sunhemp, buckwheat, clover, rye, and vetch. Common mistakes to avoid include repeating same crop family, no legume inclusion, and ignoring market demand."},
        
        {"keywords": ["weather", "climate", "rainfall", "temperature", "season"], "response": "🌤️ For weather and climate guide for farming, seasonal crop planning includes Kharif season from June to October for crops like rice, maize, cotton, sugarcane, and groundnut requiring rainfall of 75-150 cm and temperature of 25-35 degrees Celsius. Rabi season from October to March for crops like wheat, barley, mustard, and chickpea requiring rainfall of 10-20 cm and temperature of 10-25 degrees Celsius. Zaid season from April to June for short duration crops like watermelon, cucumber, and muskmelon requiring irrigation. For climate change adaptation strategies, use climate-resilient varieties, adjust planting dates, grow drought-tolerant crops, construct water harvesting structures, and implement agro-forestry systems. For weather monitoring, install automatic weather station, use mobile apps like Kisan Suvidha and Meghdoot, follow IMD forecasts, and monitor soil moisture. For extreme weather management during drought, use drought-resistant varieties, apply mulching to conserve moisture, install drip irrigation, and consider cloud seeding where possible. During flood, use raised bed planting, grow submergence-tolerant varieties, create drainage channels, and get flood insurance. During heat wave, adjust sowing time, practice intercropping for shade, apply anti-transpirant sprays, and use mulching. During hailstorm, install hail nets for orchards, get crop insurance, and use protective cultivation. During frost, apply irrigation before frost, generate smoke, cover crops, and use wind machines. Weather-based crop insurance like Pradhan Mantri Fasal Bima Yojana or PMFBY covers yield losses and offers weather index insurance. Useful weather apps include Meghdoot from ICAR, Kisan Suvidha, Weather Union, and AccuWeather for Farmers."}
    ],
    "fallback": "🤔 I can help with many agricultural topics including crop management for rice, wheat, maize, pulses, and oilseeds covering sowing time, varieties, and spacing. I provide pest and disease management to identify pests and diseases with control measures including chemical, biological, and organic options. I offer fertilizer and nutrient management with NPK recommendations, organic manures, and bio-fertilizers. I provide irrigation and water management including methods like drip, sprinkler, and flood along with water saving techniques. I cover organic farming including organic inputs preparation and certification process. I help with crop rotation and planning including rotation principles and cropping systems. I provide weather and climate information for seasonal planning and climate adaptation. I cover soil management including soil testing, soil health cards, and conservation practices. I assist with post-harvest management including storage, processing, and value addition. I also cover marketing and economics including MSP, government schemes, and profitability analysis. Please try asking specific questions like how to control rice stem borer, fertilizer schedule for wheat, drip irrigation subsidy details, organic pest control methods, crop rotation for vegetables, or market price of rice."
}

# --------------------------------------------------
# QUERY PROCESSOR
# --------------------------------------------------
def process_query(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    
    # Check for price query
    if any(word in text for word in ["price", "rate", "market", "cost"]):
        for crop in ["rice", "wheat", "maize", "cotton", "sugarcane"]:
            if crop in text:
                prices = get_market_prices(crop)
                return f"💰 The current market price for {crop.title()} shows a minimum of ₹{prices['min']} per quintal, maximum of ₹{prices['max']} per quintal, and average of ₹{prices['avg']} per quintal. The market trend is {prices['trend']}. Please note that these prices vary by location and quality, so it is recommended to check your local mandi for exact rates before selling your produce."
    
    # Check for fertilizer calculator
    if "calculate fertilizer" in text or "fertilizer calculator" in text:
        match = re.search(r"(rice|wheat|maize|cotton).*?(\d+(?:\.\d+)?)\s*hectares?", text)
        if match:
            crop = match.group(1)
            area = float(match.group(2))
            result = calculate_fertilizer(crop, area)
            if result:
                return f"📊 For {crop.title()} cultivation on {area} hectares, you will need approximately {result['urea_kg']:.0f} kg of urea, {result['dap_kg']:.0f} kg of DAP, and {result['mop_kg']:.0f} kg of MOP. Please note that these are approximate recommendations and should be adjusted based on your soil test results for optimal crop production."
            else:
                return "Sorry, the fertilizer calculator currently supports rice, wheat, maize, and cotton only. Please specify one of these crops for accurate calculation."
    
    # Check for weather
    if "weather" in text or "temperature" in text:
        condition, temp, humidity = get_weather_data()
        return f"🌡️ The current weather conditions show {condition} skies with temperature at {temp} degrees Celsius and humidity at {humidity} percent. This data is simulated for demonstration purposes. For accurate weather information, please refer to your local weather department or use apps like Meghdoot or Kisan Suvidha."
    
    # Check for irrigation
    if "irrigation" in text or "drip" in text or "sprinkler" in text:
        for item in DATA["responses"]:
            if "irrigation" in item["keywords"]:
                return item["response"]
    
    # Check for organic
    if "organic" in text:
        for item in DATA["responses"]:
            if "organic" in item["keywords"]:
                return item["response"]
    
    # Check for crop rotation
    if "rotation" in text:
        for item in DATA["responses"]:
            if "crop rotation" in item["keywords"]:
                return item["response"]
    
    # Regular response matching
    for item in DATA["responses"]:
        for keyword in item["keywords"]:
            if keyword in text:
                return item["response"]
    
    return DATA["fallback"]

# --------------------------------------------------
# QUICK COMMAND BUTTONS
# --------------------------------------------------
st.markdown("### 🔍 Quick Questions")

col1, col2, col3, col4 = st.columns(4)

quick_queries = {
    "🌾 Rice": "rice farming tips",
    "🌾 Wheat": "wheat cultivation",
    "🌽 Maize": "maize production",
    "🐛 Pests": "pest control methods",
    "🦠 Diseases": "disease management",
    "🧪 Fertilizer": "fertilizer schedule",
    "💧 Irrigation": "irrigation methods",
    "🌱 Organic": "organic farming",
    "🔄 Rotation": "crop rotation",
    "💰 Price": "market price of rice",
    "🌤️ Weather": "current weather",
    "📊 Calculate": "calculate fertilizer for rice in 1 hectare"
}

buttons_placed = 0
for query_text, query_value in quick_queries.items():
    col = [col1, col2, col3, col4][buttons_placed % 4]
    if col.button(query_text, key=f"quick_{query_text}", use_container_width=True):
        quick_prompt = query_value
        st.session_state.chat_history.append({"role": "user", "content": quick_prompt})
        with st.chat_message("user"):
            st.markdown(quick_prompt)
        response = process_query(quick_prompt)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            output = ""
            for char in response:
                output += char
                placeholder.markdown(output)
                time.sleep(0.003)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
    buttons_placed += 1

# --------------------------------------------------
# CHAT HISTORY DISPLAY
# --------------------------------------------------
st.markdown("---")
st.markdown("### 💬 Conversation")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------
user_input = st.chat_input("Ask your agriculture question... (e.g., 'rice farming tips', 'pest control for wheat', 'market price of rice')")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    response = process_query(user_input)
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        output = ""
        for char in response:
            output += char
            placeholder.markdown(output + "▌")
            time.sleep(0.003)
        placeholder.markdown(output)
    
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">
    <strong>🌾 Agri Assistant</strong> | AI-Powered Agricultural Advisory System<br>
    📊 Data based on ICAR and standard agricultural practices<br>
    💡 <strong>Tip:</strong> Be specific with your questions for better answers!<br>
    ⚠️ For critical decisions, consult local agricultural experts
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CLEAR CHAT BUTTON
# --------------------------------------------------
if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()