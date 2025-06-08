import time
from appvega.utils import start_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def hover_info(web_driver):
    svg_element = web_driver.find_element(By.CLASS_NAME, value="entry-info-popup")
    actions = ActionChains(web_driver)
    actions.move_to_element(svg_element).perform()


def click_on_print(web_driver):
    print_button_xpath = '//div[@class="menu"]//button[contains(.,"Print")]'
    time.sleep(2)
    print_button = web_driver.find_element(By.XPATH, print_button_xpath)
    print_button.click()


def get_times(web_driver):
    times = web_driver.find_elements(by=By.CLASS_NAME, value="periods-overview-sub-item")
    return [time.text for time in times if
            time.get_attribute("data-selected") == "true" and time.text != '']


def get_word_id(web_driver):
    return web_driver.find_element(by=By.CLASS_NAME, value="entry-id").text[3:]


def get_word_transliteration(web_driver):
    return web_driver.find_element(by=By.CLASS_NAME, value="entry-transliteration").text


def get_word_category(web_driver):
    try:
        return ", ".join(web_driver.find_element(by=By.CLASS_NAME, value="entry-natures").find_elements(by=By.CLASS_NAME, value="tag"))
    except Exception as _:
        return ""


def get_publication_date(web_driver):
    return web_driver.find_element(by=By.CLASS_NAME, value="entry-save-message").text


def get_word_status(web_driver):
    return web_driver.find_element(by=By.CLASS_NAME, value="public-status").get_attribute(
        "data-status")


def get_word_hieroglyphic_spelling(web_driver):
    hieroglyphics = []
    image_section = web_driver.find_element(By.CLASS_NAME, value="entry-main-graphies")
    images = image_section.find_elements(By.CLASS_NAME, "graphy-image-bg")
    for image in images:
        attribute_style = image.get_attribute("style")
        initial_position = attribute_style.find('url("') + 5
        final_position = attribute_style.find('")')
        partial_url = attribute_style[initial_position:final_position]
        image_url = f"https://app.vega-lexique.fr/{partial_url}"
        hieroglyphics.append(image_url)
    return hieroglyphics


def get_word_translation(web_driver, pos):
    translation_section = web_driver.find_element(by=By.CLASS_NAME, value="entry-data")
    return translation_section.find_elements(by=By.CLASS_NAME, value="entry-nuance")[pos].text


def get_word_dictionaries_lexicons_and_references(web_driver):
    references_section = web_driver.find_elements(by=By.CLASS_NAME, value="entry-dictionary-group")
    references = {}
    for reference in references_section:
        title = reference.find_element(by=By.CLASS_NAME, value="entry-dictionary-group-title")
        labels = reference.find_elements(by=By.CLASS_NAME, value="entry-dictionary-label")
        values = reference.find_elements(by=By.CLASS_NAME, value="entry-dictionary-value")
        info = []
        for label, value in zip(labels, values):
            info.append({
                "label": label.text,
                "value": value.text
            })
        references[title.text] = info
    return references


def get_word_dictionaries(web_driver):
    ...


def get_word_lexicons_and_indexes(web_driver):
    ...


def get_word_other_references(web_driver):
    ...


def get_word_comments(web_driver):
    try:
        comment_section = web_driver.find_element(by=By.ID, value="comments")
        return [comment.text for comment in
                comment_section.find_elements(by=By.TAG_NAME, value="span")]
    except Exception as e:
        return []


def get_word_entry_author(web_driver):
    try:
        return web_driver.find_element(by=By.ID, value="entry-authors").find_element(by=By.TAG_NAME, value="span").text
    except Exception as e:
        return ""
    

def download_data(target_url):
    driver = start_browser()
    driver.get(target_url)
    time.sleep(1)

    times = []
    try:
        driver.find_element(by=By.CLASS_NAME, value="periods-overview").click()
        times = get_times(driver)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
    except Exception as e:
        pass

    hover_info(driver)
    publication_date = get_publication_date(driver)
    id_ = get_word_id(driver)
    time.sleep(1)

    click_on_print(driver)
    time.sleep(1)
    data = {
        "id": id_,
        "transliteration": get_word_transliteration(driver),
        "publication_date": publication_date,
        "status": get_word_status(driver),
        "category": get_word_category(driver),
        "image": get_word_hieroglyphic_spelling(driver),
        "DE": get_word_translation(driver, 0),
        "AR": get_word_translation(driver, 1),
        "EN": get_word_translation(driver, 2),
        "FR": get_word_translation(driver, 3),
        "times": times,
        "comment": get_word_comments(driver),
        "author": get_word_entry_author(driver)
    }
    data.update(get_word_dictionaries_lexicons_and_references(driver))
    return data
