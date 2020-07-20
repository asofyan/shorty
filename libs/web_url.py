class WebUrl:

    def __init__(self, connection):
        self.connection = connection

    def get_url_by_code(self, code):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT URL FROM WEB_URL WHERE S_URL = %s;', [code])
            result = cursor.fetchone()
            if result:
                return result[0]


    def update_counter(self, short_url, browser_dict, platforms_dict, counter):
        counter_sql = "\
            UPDATE {tn} SET COUNTER = COUNTER + {og_counter} , CHROME = CHROME + {og_chrome} , FIREFOX = FIREFOX+{og_firefox} ,\
            SAFARI = SAFARI+{og_safari} , OTHER_BROWSER =OTHER_BROWSER+ {og_oth_brow} , ANDROID = ANDROID +{og_andr} , IOS = IOS +{og_ios},\
            WINDOWS = WINDOWS+{og_windows} , LINUX = LINUX+{og_linux}  , MAC =MAC+ {og_mac} , OTHER_PLATFORM =OTHER_PLATFORM+ {og_plat_other} WHERE S_URL = %s;".\
            format(tn = "WEB_URL" , og_counter = counter , og_chrome = browser_dict['chrome'] , og_firefox = browser_dict['firefox'],\
            og_safari = browser_dict['safari'] , og_oth_brow = browser_dict['other'] , og_andr = platforms_dict['android'] , og_ios = platforms_dict['iphone'] ,\
            og_windows = platforms_dict['windows'] , og_linux = platforms_dict['linux'] , og_mac = platforms_dict['macos'] , og_plat_other = platforms_dict['other'])

        with self.connection.cursor() as cursor:
            res_update = cursor.execute(counter_sql, (short_url, ))

        self.connection.commit()