"""
KrishiMitra Disease Insights Database
Complete treatment pathways, pesticides, and guidance for farmers
"""

DISEASE_INSIGHTS = {
    "Apple___Apple_scab": {
        "severity": "medium",
        "cure_timeline": "2-4 weeks with treatment",
        "description": {
            "en": "Apple scab is a fungal disease caused by Venturia inaequalis. It affects leaves and fruits, causing dark, velvety, scabby spots. Most severe in cool, wet seasons.",
            "hi": "एप्पल स्कैब Venturia inaequalis द्वारा कारित एक फफुंदी रोग है। यह पत्तियों और फलों को प्रभावित करता है, गहरे, मखमली, खुरदरे धब्बे पैदा करते हुए।",
            "kn": "ಆಪಲ್ ಸ್ಕ್ಯಾಬ್ Venturia inaequalis ಕಾರಿತ ಫಂಗಲ್ ರೋಗವಾಗಿದೆ। ಇದು ಎಲೆ ಮತ್ತು ಫಲಿತಾಂಶವನ್ನು ಪ್ರಭಾವಿಸುತ್ತದೆ."
        },
        "symptoms": {
            "en": "Dark brown spots on leaves and fruits, olive-green velvety surface, leaves may wilt and fall off early",
            "hi": "पत्तियों और फलों पर गहरे भूरे धब्बे, जैतून-हरी मखमली सतह, पत्तियां सूख कर जल्दी गिर सकती हैं",
            "kn": "ಎಲೆ ಮತ್ತು ಫಲಿತಾಂಶದ ಮೇಲೆ ಗಾಢ ಕಂದು ಗುರುತುಗಳು"
        },
        "pesticides": [
            {
                "name": "Captan 50 WP",
                "dosage": "2.5-3 kg per hectare",
                "spray_interval": "Every 15 days from bud break to post-bloom",
                "precautions": "Use gloves and mask. Do not spray during rain or within 24 hours before rain.",
                "cost_range": "₹800-1200 per kg"
            },
            {
                "name": "Myclobutanil 10 EC",
                "dosage": "1-1.2 liters per hectare",
                "spray_interval": "Every 20-25 days starting early spring",
                "precautions": "Avoid contact with skin. Spray in evening.",
                "cost_range": "₹1500-2000 per liter"
            },
            {
                "name": "Sulfur 80 WP",
                "dosage": "3 kg per hectare",
                "spray_interval": "Every 10-15 days",
                "precautions": "Do not mix with oil sprays. Avoid high temperatures.",
                "cost_range": "₹300-400 per kg"
            }
        ],
        "organic_treatment": {
            "en": "Use neem oil (3%) spray every 10 days. Apply sulfur dust. Remove infected leaves immediately. Ensure 40% tree canopy opening for air circulation. Prune diseased branches.",
            "hi": "नीम का तेल (3%) का छिड़काव हर 10 दिन में करें। सल्फर डस्ट लगाएं। संक्रमित पत्तियों को तुरंत हटाएं। वायु संचार के लिए 40% पेड़ की शाखाओं को खुला रखें।",
            "kn": "ನೀಮ್ ತೈಲ (3%) ಸ್ಪ್ರೇ ಪ್ರತಿ 10 ದಿನಗಳಿಗೆ ಬಳಸಿ. ಸಲ್ಫರ್ ಧೂಳು ಹರಡಿ."
        },
        "steps_to_cure": [
            {
                "step": 1,
                "action": "Early Detection",
                "details": "Check trees weekly during wet season. Look for small olive-green spots on young leaves."
            },
            {
                "step": 2,
                "action": "Immediate Pruning",
                "details": "Remove all infected leaves and branches. Burn or bury them away from orchard."
            },
            {
                "step": 3,
                "action": "First Spray",
                "details": "Start preventive spraying at bud break. Use Captan or Myclobutanil as first choice."
            },
            {
                "step": 4,
                "action": "Regular Monitoring",
                "details": "Inspect trees every 7-10 days. Repeat sprays every 15-20 days as per schedule."
            },
            {
                "step": 5,
                "action": "Canopy Management",
                "details": "Remove lower branches to allow 40% light penetration and improve air circulation."
            },
            {
                "step": 6,
                "action": "Post-Harvest Care",
                "details": "Clean fallen leaves and twigs. Do not leave infected material in orchard. Destroy completely."
            }
        ],
        "prevention": {
            "en": "Plant resistant varieties (like Gala, Fuji). Ensure proper spacing (6-8 meters). Prune for good air circulation. Avoid overhead irrigation. Monitor weather for high humidity.",
            "hi": "प्रतिरोधी किस्में (गाला, फूजी) लगाएं। उचित दूरी (6-8 मीटर) सुनिश्चित करें। अच्छी हवा के लिए छंटाई करें।",
            "kn": "ಪ್ರತಿರೋಧಕ ಪ್ರಭೇದಗಳನ್ನು ನಾಟಿ ಮಾಡಿ."
        },
        "nearest_help": {
            "en": "Contact your local Agricultural Extension Officer. Visit nearest Horticulture Department office. Call KVK (Krishi Vigyan Kendra) for expert advice.",
            "hi": "अपने स्थानीय कृषि विस्तार अधिकारी से संपर्क करें। निकटतम बागवानी विभाग कार्यालय जाएं।",
            "kn": "ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಸ್ತರಣೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ."
        }
    },
    "Tomato___Late_blight": {
        "severity": "high",
        "cure_timeline": "1-3 weeks with intensive treatment",
        "description": {
            "en": "Late blight caused by Phytophthora infestans. A destructive fungal disease affecting leaves, stems, and fruits. Spreads rapidly in cool, wet conditions.",
            "hi": "Phytophthora infestans द्वारा कारित लेट ब्लाइट। एक विनाशकारी फफुंदी रोग जो पत्तियों, तनों और फलों को प्रभावित करता है। ठंडे, गीले स्थितियों में तेजी से फैलता है।",
            "kn": "Phytophthora infestans ಕಾರಿತ ಲೇಟ್ ಬ್ಲೈಟ್. ಒಂದು ವಿನಾಶಕಾರಿ ಫಂಗಲ್ ರೋಗ."
        },
        "symptoms": {
            "en": "Water-soaked dark spots on leaves, white moldy growth on leaf undersides, rapid leaf yellowing and wilting, fruit develops brown sunken spots",
            "hi": "पत्तियों पर पानी से भिगोए हुए गहरे धब्बे, पत्ती के नीचे सफेद मोल्डी वृद्धि, पत्तियां तेजी से पीली पड़ जाती हैं और मुरझा जाती हैं",
            "kn": "ಎಲೆಗಳಿನ ಮೇಲೆ ಜಲಸಿಂಚಿತ ಗಾಢ ಗುರುತುಗಳು"
        },
        "pesticides": [
            {
                "name": "Mancozeb 75 WP",
                "dosage": "2.5 kg per hectare",
                "spray_interval": "Every 7-10 days starting from first symptoms",
                "precautions": "Use mask and gloves. Do not apply during rain or high humidity.",
                "cost_range": "₹400-600 per kg"
            },
            {
                "name": "Metalaxyl 8% + Mancozeb 64% WP",
                "dosage": "2.5 kg per hectare",
                "spray_interval": "Every 5-7 days in severe outbreak",
                "precautions": "This is systemic+contact fungicide. Highly effective against late blight.",
                "cost_range": "₹1200-1500 per kg"
            },
            {
                "name": "Chlorothalonil 75 WP",
                "dosage": "2 kg per hectare",
                "spray_interval": "Every 10-14 days",
                "precautions": "Wash hands thoroughly after application.",
                "cost_range": "₹600-800 per kg"
            }
        ],
        "organic_treatment": {
            "en": "Spray copper sulfate (0.5%) twice weekly. Use Bacillus subtilis-based bioagents. Remove infected leaves immediately. Ensure canopy drying by pruning lower leaves. Use drip irrigation to keep leaves dry.",
            "hi": "कॉपर सल्फेट (0.5%) का सप्ताह में दो बार छिड़काव करें। Bacillus subtilis आधारित जैव कारकों का उपयोग करें। संक्रमित पत्तियों को तुरंत हटाएं।",
            "kn": "ತಾಮ್ರ ಸಲ್ಫೇಟ್ (0.5%) ಸ್ಪ್ರೇ ಬಿ ನಿಂದ ಸ್ವಿಂಗ."
        },
        "steps_to_cure": [
            {
                "step": 1,
                "action": "Emergency Response",
                "details": "At first sign of water-soaked spots, immediately spray with Metalaxyl+Mancozeb mixture."
            },
            {
                "step": 2,
                "action": "Remove Infected Parts",
                "details": "Remove all infected leaves and infected fruit. Do not compost - burn away from field."
            },
            {
                "step": 3,
                "action": "Intensive Spraying",
                "details": "Spray every 5-7 days for first 2 weeks. Use different fungicides in rotation to prevent resistance."
            },
            {
                "step": 4,
                "action": "Canopy Pruning",
                "details": "Remove lower leaves (up to 30 cm) to allow sunlight and air circulation. This is critical."
            },
            {
                "step": 5,
                "action": "Irrigation Management",
                "details": "Stop overhead watering immediately. Switch to drip irrigation. Water only at soil level in early morning."
            },
            {
                "step": 6,
                "action": "Field Sanitation",
                "details": "Remove and destroy all dead leaves, fallen fruits, and plant debris daily."
            }
        ],
        "prevention": {
            "en": "Plant on raised beds. Use disease-free seeds/seedlings. Maintain 60cm spacing. Avoid overhead irrigation. Scout fields regularly. Plant resistant varieties when available.",
            "hi": "क्यारियों में रोपण करें। रोग-मुक्त बीज/पौधे का उपयोग करें। 60cm दूरी बनाए रखें।",
            "kn": "ಮೇಲೆತ್ತುವ ಕೆಲೆ ಮೇಲೆ ನಾಟಿ ಮಾಡಿ."
        },
        "nearest_help": {
            "en": "Rush to nearest Agricultural Science Centre. Emergency contact: Your State Department of Horticulture/Agriculture. Seek expert advice immediately - late blight spreads fast.",
            "hi": "निकटतम कृषि विज्ञान केंद्र जाएं। आपातकालीन संपर्क: आपके राज्य का कृषि विभाग।",
            "kn": "ಹತ್ತಿರದ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರಕ್ಕೆ ಯೆ."
        }
    },
    "Potato___Early_blight": {
        "severity": "medium",
        "cure_timeline": "2-3 weeks with proper treatment",
        "description": {
            "en": "Early blight caused by Alternaria solani. Fungal disease affecting potato leaves. Concentric rings appear on infected leaves. Less damaging than late blight.",
            "hi": "Alternaria solani द्वारा कारित अर्ली ब्लाइट। आलू की पत्तियों को प्रभावित करने वाला फफुंदी रोग। संक्रमित पत्तियों पर संकेंद्रित छल्ले दिखाई देते हैं।",
            "kn": "Alternaria solani ಕಾರಿತ ಆರ್ಲಿ ಬ್ಲೈಟ್."
        },
        "symptoms": {
            "en": "Brown spots with concentric rings on lower leaves, yellow halo around spots, spots enlarge and coalesce, lower leaves wither but plant survives",
            "hi": "निचली पत्तियों पर संकेंद्रित छल्लों के साथ भूरे धब्बे, धब्बों के चारों ओर पीला प्रभामंडल, धब्बे बढ़ते हैं और मिल जाते हैं",
            "kn": "ಕೆಳ ಎಲೆಗಳಿನ ಮೇಲೆ ಸಂಕೇಂದ್ರಿತ ರಿಂಗ್‌ಗಳೊಂದಿಗೆ ಭೂರೆ ಗುರುತುಗಳು"
        },
        "pesticides": [
            {
                "name": "Mancozeb 75 WP",
                "dosage": "2-2.5 kg per hectare",
                "spray_interval": "Every 10-14 days starting from first symptoms",
                "precautions": "Use protective equipment. Do not spray within 48 hours of rain.",
                "cost_range": "₹400-600 per kg"
            },
            {
                "name": "Chlorothalonil 75 WP",
                "dosage": "2-2.5 kg per hectare",
                "spray_interval": "Every 10-12 days",
                "precautions": "Avoid skin contact. Spray in early morning or late evening.",
                "cost_range": "₹600-800 per kg"
            }
        ],
        "organic_treatment": {
            "en": "Spray Bacillus subtilis suspension every 10 days. Use copper oxide (0.3%) spray. Remove lower infected leaves regularly. Ensure good drainage and avoid excess moisture.",
            "hi": "Bacillus subtilis निलंबन हर 10 दिन में छिड़कें। कॉपर ऑक्साइड (0.3%) स्प्रे का उपयोग करें।",
            "kn": "Bacillus subtilis ಸಸ್ಪೆನ್ಷನ್ ಪ್ರತಿ 10 ದಿನಗಳಿಗೆ ಸ್ಪ್ರೇ ಮಾಡಿ."
        },
        "steps_to_cure": [
            {
                "step": 1,
                "action": "Early Detection",
                "details": "Check lower leaves regularly for concentric ring spots starting from flowering stage."
            },
            {
                "step": 2,
                "action": "Remove Infected Leaves",
                "details": "Remove all spotted lower leaves (up to 30cm height) and destroy them outside the field."
            },
            {
                "step": 3,
                "action": "First Fungicide Spray",
                "details": "Spray Mancozeb or Chlorothalonil as soon as first symptoms appear."
            },
            {
                "step": 4,
                "action": "Repeat Sprays",
                "details": "Continue spraying every 10-14 days. Use different products in rotation."
            },
            {
                "step": 5,
                "action": "Drainage Management",
                "details": "Ensure field has good drainage. Avoid waterlogging as it promotes fungal growth."
            },
            {
                "step": 6,
                "action": "Harvest Early",
                "details": "If infection is severe, harvest 2-3 weeks early before tubers are affected."
            }
        ],
        "prevention": {
            "en": "Use certified seed potatoes. Remove volunteer plants. Ensure 50cm spacing. Practice crop rotation (2-3 years). Plant resistant varieties. Maintain field sanitation.",
            "hi": "प्रमाणित बीज आलू का उपयोग करें। स्वयंसेवी पौधों को हटाएं। 50cm दूरी सुनिश्चित करें।",
            "kn": "ಪ್ರಮಾಣೀಕೃತ ಬೀಜ ಆಲೂಗಡ್ಡೆ ಬಳಸಿ."
        },
        "nearest_help": {
            "en": "Contact District Agriculture Officer. Visit nearest Potato Research Station. Call your State Seed Development Organization for resistant variety information.",
            "hi": "जिला कृषि अधिकारी से संपर्क करें। निकटतम आलू अनुसंधान स्टेशन जाएं।",
            "kn": "ಜಿಲ್ಲೆ ಕೃಷಿ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ."
        }
    },
    "Pepper,_bell___Bacterial_spot": {
        "severity": "medium",
        "cure_timeline": "3-4 weeks with treatment",
        "description": {
            "en": "Bacterial spot caused by Xanthomonas species. Bacterial disease affecting pepper leaves and fruits. Small water-soaked spots that become necrotic. Spreads in warm, wet conditions.",
            "hi": "Xanthomonas प्रजातियों द्वारा कारित बैक्टीरियल स्पॉट। शिमला मिर्च की पत्तियों और फलों को प्रभावित करने वाला बैक्टीरियल रोग।",
            "kn": "Xanthomonas ಪ್ರಜಾತಿಗಳ ದ್ವಾರಾ ಕಾರಿತ ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಸ್ಪಾಟ್."
        },
        "symptoms": {
            "en": "Small yellow-brown spots with water-soaked appearance on leaves and fruits, spots have oily appearance, leaves gradually yellow and drop, fruit becomes unmarketable",
            "hi": "पत्तियों और फलों पर पानी से भिगोए गए छोटे पीले-भूरे धब्बे, धब्बों का तैलीय दिखावट, पत्तियां धीरे-धीरे पीली पड़ जाती हैं और गिरती हैं",
            "kn": "ಎಲೆ ಮತ್ತು ಫಲಿತಾಂಶದ ಮೇಲೆ ಸಣ್ಣ ಪೀತ-ಕಂದು ಗುರುತುಗಳು"
        },
        "pesticides": [
            {
                "name": "Copper Oxychloride 50 WP",
                "dosage": "2.5-3 kg per hectare",
                "spray_interval": "Every 10-12 days starting from transplanting",
                "precautions": "Use gloves and mask. Do not mix with oil sprays.",
                "cost_range": "₹400-500 per kg"
            },
            {
                "name": "Streptocycline 10 EC",
                "dosage": "750 ml per hectare",
                "spray_interval": "Every 7-10 days at first sign of disease",
                "precautions": "Rotate with copper products. Use early morning or evening.",
                "cost_range": "₹3000-3500 per liter"
            }
        ],
        "organic_treatment": {
            "en": "Spray Bordeaux mixture (1%) weekly. Use copper sulfate solution. Apply bio-fungicide Bacillus subtilis. Remove infected leaves and fruits immediately. Ensure good drainage and avoid overhead watering.",
            "hi": "Bordeaux मिश्रण (1%) साप्ताहिक रूप से स्प्रे करें। कॉपर सल्फेट समाधान का उपयोग करें।",
            "kn": "ಬೋರ್ಡೋ ಮಿಶ್ರಣ (1%) ಸಾಪ್ತಾಹಿಕವಾಗಿ ಸ್ಪ್ರೇ ಮಾಡಿ."
        },
        "steps_to_cure": [
            {
                "step": 1,
                "action": "Sanitation First",
                "details": "Remove all infected leaves and fruits immediately. Sterilize pruning tools after each cut."
            },
            {
                "step": 2,
                "action": "Start Preventive Sprays",
                "details": "Begin sprays from 30 days after transplanting with Copper Oxychloride."
            },
            {
                "step": 3,
                "action": "Weekly Monitoring",
                "details": "Check plants every 3-4 days for new symptoms during wet season."
            },
            {
                "step": 4,
                "action": "Drainage Improvement",
                "details": "Ensure adequate drainage. Avoid overhead irrigation. Water only at soil level in morning."
            },
            {
                "step": 5,
                "action": "Antibiotic Spray",
                "details": "If disease persists after 2 weeks, use Streptocycline spray every 7 days."
            },
            {
                "step": 6,
                "action": "Field Sanitation",
                "details": "Remove plant debris, fallen leaves, and unmarketable fruits daily from field."
            }
        ],
        "prevention": {
            "en": "Use disease-free seeds. Maintain spacing (50-60cm). Practice crop rotation (minimum 2 years). Avoid overhead irrigation. Scout fields weekly. Plant in well-drained fields.",
            "hi": "रोग-मुक्त बीजों का उपयोग करें। 50-60cm दूरी बनाएं। फसल चक्र अभ्यास करें।",
            "kn": "ರೋಗ-ಮುಕ್ತ ಬೀಜಗಳನ್ನು ಬಳಸಿ. 50-60cm ಅಂತರ ನಿರ್ವಹಿಸಿ."
        },
        "nearest_help": {
            "en": "Contact Vegetable Science Department of nearby Agricultural University. Visit District Horticulture Office. Consult with Extension Officer about resistant pepper varieties.",
            "hi": "निकटवर्ती कृषि विश्वविद्यालय के सब्जी विज्ञान विभाग से संपर्क करें।",
            "kn": "ಹತ್ತಿರದ ಸಾವಿರಗಿರಿ ವಿಶ್ವವಿದ್ಯಾಲಯದ ತರಕಾರಿ ವಿಜ್ಞಾನ ವಿಭಾಗವನ್ನು ಸಂಪರ್ಕಿಸಿ."
        }
    }
}

# Extended data for remaining 34 diseases - placeholder structure
# In production, each would have full details like above

def get_disease_insight(disease_name: str, lang: str = 'en') -> dict:
    """
    Get comprehensive disease insight for a given disease
    
    Args:
        disease_name: Disease name from CLASS_NAMES
        lang: Language code ('en', 'hi', 'kn')
    
    Returns:
        Dictionary with complete disease information
    """
    if disease_name in DISEASE_INSIGHTS:
        return DISEASE_INSIGHTS[disease_name]
    else:
        # Return generic template for diseases not yet documented
        return {
            "severity": "unknown",
            "cure_timeline": "Consult expert",
            "description": {
                "en": f"Disease: {disease_name.replace('_', ' ')}. Detailed information not yet available. Please consult a local expert.",
                "hi": f"रोग: {disease_name.replace('_', ' ')}। विस्तृत जानकारी अभी उपलब्ध नहीं है।",
                "kn": f"ರೋಗ: {disease_name.replace('_', ' ')}. ವಿಸ್ತೃತ ಮಾಹಿತಿ ಇನ್ನೂ ಲಭ್ಯವಾಗಿಲ್ಲ."
            },
            "symptoms": {
                "en": "Consult local agricultural expert for symptom details.",
                "hi": "लक्षणों के लिए स्थानीय कृषि विशेषज्ञ से परामर्श लें।",
                "kn": "ಲಕ್ಷಣಗಳ ವಿವರಣೆಗಾಗಿ ಸ್ಥಳೀಯ ಕೃಷಿ ಪರಿಣಮಸ್ವಾಮಿಗೆ ಸಂಪರ್ಕಿಸಿ."
            },
            "pesticides": [],
            "organic_treatment": {
                "en": "Contact your local Agricultural Extension Office",
                "hi": "अपने स्थानीय कृषि विस्तार कार्यालय से संपर्क करें",
                "kn": "ನಿಮ್ಮ ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಸ್ತರಣೆ ಕಚೇರಿಗೆ ಸಂಪರ್ಕಿಸಿ"
            },
            "steps_to_cure": [
                {
                    "step": 1,
                    "action": "Consult Expert",
                    "details": "Please visit your nearest agricultural science center or extension office."
                }
            ],
            "prevention": {
                "en": "Maintain good field hygiene and crop rotation practices.",
                "hi": "अच्छी खेत स्वच्छता और फसल चक्र प्रथाओं को बनाए रखें।",
                "kn": "ಉತ್ತಮ ಹೊಲ ನೈರ್ಮಲ್ಯ ಮತ್ತು ಪುಷ್ಪ ಚಕ್ರ ಅಭ್ಯಾಸಗಳನ್ನು ನಿರ್ವಹಿಸಿ."
            },
            "nearest_help": {
                "en": "Contact your State Agricultural Department for comprehensive guidance.",
                "hi": "व्यापक मार्गदर्शन के लिए अपने राज्य कृषि विभाग से संपर्क करें।",
                "kn": "ವ್ಯಾಪಕ ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ನಿಮ್ಮ ರಾಜ್ಯ ಕೃಷಿ ವಿಭಾಗವನ್ನು ಸಂಪರ್ಕಿಸಿ."
            }
        }


def format_disease_insight_for_display(disease_name: str, lang: str = 'en') -> str:
    """
    Format disease insight as farmer-friendly readable text
    """
    insight = get_disease_insight(disease_name, lang)
    
    text = f"# {disease_name.replace('_', ' ')}\n\n"
    
    # Severity and timeline
    text += f"**⚠️ Severity Level:** {insight.get('severity', 'unknown').upper()}\n"
    text += f"**⏱️ Expected Cure Timeline:** {insight.get('cure_timeline', 'Contact expert')}\n\n"
    
    # Description
    if isinstance(insight.get('description'), dict):
        text += f"## Description\n{insight['description'].get(lang, insight['description'].get('en'))}\n\n"
    
    # Symptoms
    if isinstance(insight.get('symptoms'), dict):
        text += f"## Key Symptoms\n{insight['symptoms'].get(lang, insight['symptoms'].get('en'))}\n\n"
    
    # Pesticides
    if insight.get('pesticides'):
        text += f"## Recommended Chemical Treatments\n"
        for pest in insight['pesticides']:
            text += f"\n### {pest['name']}\n"
            text += f"- **Dosage:** {pest.get('dosage', 'As per label')}\n"
            text += f"- **Spray Interval:** {pest.get('spray_interval', 'As needed')}\n"
            text += f"- **Cost:** {pest.get('cost_range', 'Variable')}\n"
            text += f"- **⚠️ Precautions:** {pest.get('precautions', 'Follow label instructions')}\n"
    
    # Organic treatment
    if isinstance(insight.get('organic_treatment'), dict):
        text += f"\n## Organic/Natural Treatment\n{insight['organic_treatment'].get(lang, insight['organic_treatment'].get('en'))}\n"
    
    # Step-by-step cure
    if insight.get('steps_to_cure'):
        text += f"\n## Step-by-Step Treatment Plan\n"
        for step in insight['steps_to_cure']:
            text += f"\n**Step {step['step']}: {step['action']}**\n"
            text += f"{step['details']}\n"
    
    # Prevention
    if isinstance(insight.get('prevention'), dict):
        text += f"\n## Prevention for Future\n{insight['prevention'].get(lang, insight['prevention'].get('en'))}\n"
    
    # Nearest help
    if isinstance(insight.get('nearest_help'), dict):
        text += f"\n## 🆘 Need Expert Help?\n{insight['nearest_help'].get(lang, insight['nearest_help'].get('en'))}\n"
    
    return text
