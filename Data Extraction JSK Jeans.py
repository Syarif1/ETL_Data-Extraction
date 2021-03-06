from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import time
import datetime
import os
import progressbar

class jsk:

    def __init__(self):

        cookies = dict(cookie="......")

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': cookies,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
            }

        widgets = [
            progressbar.Percentage(),
            progressbar.Bar(marker='\x1b[32m*\x1b[39m',left=' | ', right=' | ',fill='█', fill_left=True),
            progressbar.AbsoluteETA(format_not_started=False)
        ]


        print('\n____________JSK Jeans Scraping and Checking Stock Real Time____________\n\n')

        while True:
            try:
                action = int(input('Please select tools below :\n\n1. Scraping tools\n2. Checking stock tools\n\nPlease Input Your Option :\n\n'))

                getPria = self.getUrlPria(headers)
                time.sleep(0.2)
                getWanita = self.getUrlWanita(headers)
                time.sleep(0.2)

                urlpria = pd.read_csv('URL Order JSK Jeans Pria_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv')
                urlwanita = pd.read_csv('URL Order JSK Jeans Wanita_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv')
                mergeurl = pd.concat([urlpria, urlwanita], ignore_index=True)

                mergeurl.to_csv('URL Order JSK Jeans Pria & Wanita_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv', index = False)

                if action == 1:
                    print('\nScrape process is loading, please wait for moment.......\n\n')
                    scrape = self.scrape(widgets, cookies)
                elif action == 2 :
                    print('Checking stock is running, please wait...\n\n')
                    getstock = self.checkStock(widgets, cookies)
                else:
                    print("\nHanya angka 1 atau 2 saja\n")
                    continue
            except ValueError:
                print("\nHanya angka 1 atau 2 saja\n")
                #kembali ke input
                continue
            else:
                #action was successfully parsed!
                #we're ready to exit the loop.
                break


    def getUrlPria(self, headers):

        try:
            results_df = pd.DataFrame() # ini harus selalu di taruh di atas <-- initialize a results dataframe to dump/store the data you collect after each iteration
            url = 'https://www.jskjeans.co.id/store?page=.......'
            time.sleep(0.1)
            response = requests.get(url, headers=headers)
            html = BeautifulSoup(response.content, 'html.parser')
            body = html.findAll('div', class_='panel-body pb-sm')

            kodeProduk = []
            judulProduk = []
            url = []
            for elem in body:
                kode = elem.find('h5').text
                title = elem.find('a').text
                kode = kode.replace(title,'')
                href = elem.find('a').get('href')


                kodeProduk.append(kode)
                judulProduk.append(title)
                url.append('https://www.jskjeans.co.id' + href)


            data = pd.DataFrame({
                'KODE PRODUK' : kodeProduk,
                'JUDUL PRODUK': judulProduk,
                'URL PRODUK' : url
                })

            # length BEFOR removing duplicates
            print('\n\nTotal data url pria sebelum remove duplicate ' + str(len(data)) + ' produk')

            # sorting by first name 
            data.sort_values('KODE PRODUK', inplace=True) 
            
            # dropping duplicate values 
            data.drop_duplicates(keep=False, inplace=True) 
            
            # length after removing duplicates 
            print('Total data url pria setelah remove duplicate ' + str(len(data)) + ' produk')

            results_df = results_df.append(data).reset_index(drop=True) #<-- dumping that data into a results dataframe
            results_df.to_csv('URL Order JSK Jeans Pria_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv', index=False, encoding="utf-8")#<-- writing the results dataframe to csv
   
        except UnboundLocalError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass
        except KeyError:
            pass
        except TypeError:
            pass

        
    def getUrlWanita(self, headers):
        try:
            df_wanita = pd.DataFrame() # ini harus selalu di taruh di atas <-- initialize a results dataframe to dump/store the data you collect after each iteration
            url = 'https://www.jskjeans.co.id/store?page=...........'

            time.sleep(0.1)
            response = requests.get(url, headers=headers)
            html = BeautifulSoup(response.content, 'html.parser')
            body = html.findAll('div', class_='panel-body pb-sm')

            kodeProduk = []
            judulProduk = []
            url = []
            for elem in body:
                kode = elem.find('h5').text
                title = elem.find('a').text
                kode = kode.replace(title,'')
                href = elem.find('a').get('href')


                kodeProduk.append(kode)
                judulProduk.append(title)
                url.append('https://www.jskjeans.co.id' + href)


            data = pd.DataFrame({
                'KODE PRODUK' : kodeProduk,
                'JUDUL PRODUK': judulProduk,
                'URL PRODUK' : url
                })

            # length BEFOR removing duplicates
            print('\n\nTotal data url wanita sebelum remove duplicate ' + str(len(data)) + ' produk')

            # sorting by first name 
            data.sort_values('KODE PRODUK', inplace=True) 
            
            # dropping duplicate values 
            data.drop_duplicates(keep=False, inplace=True) 
            
            # length after removing duplicates 
            print('Total data url wanita setelah remove duplicate ' + str(len(data)) + ' produk\n\n')

            results_df = df_wanita.append(data).reset_index(drop=True) #<-- dumping that data into a results dataframe
            results_df.to_csv('URL Order JSK Jeans Wanita_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv', index=False, encoding="utf-8")#<-- writing the results dataframe to csv


        except UnboundLocalError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass
        except KeyError:
            pass
        except TypeError:
            pass

    def checkStock(self, widgets, cookies):
        os.chdir('...........')
        results_df = pd.DataFrame() #<-- initialize a results dataframe to dump/store the data you collect after each iteration
        with open('URL Order JSK Jeans Pria & Wanita_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv','r') as f:
        #with open('URL Order JSK Jeans_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv','r') as f:
            urllist = csv.reader(f, delimiter=',')

            skipheader = next(urllist)#start loop from seconds row
            # print('\n' + str(skipheader))

            lines = list(urllist)
            print('\nTotal produk pria & wanita ' + str(len(lines))+ ' produk\n\n')
            loading = ['\x1b[32mGet stock from '+str(len(lines))+' Products\x1b[39m']
            with progressbar.ProgressBar(widgets=loading + widgets, max_value=len(lines)) as bar:
                for row in enumerate(lines,1):
                    index = row[0]
                    lis = row[1]
                    url = lis[2]
                    bar.update(index)
            
                    try:
                        r = requests.get(url, cookies=cookies)
                        html = BeautifulSoup(r.content, 'html.parser')

                        formstok = html.find('div', class_='tab-pane active')
                        ttl = formstok.find('h5', class_='mv').strong.contents[0]
                        pc = formstok.find('h5', class_='mv').strong.contents[2]
                        judul = ttl.replace('\n                                ','')
                        productcode = pc.replace('\n','')
                        productcode = productcode.replace('   ', '#')
                        productcode = productcode.replace('  ', '#')
                        productcode = productcode.replace('# ', '')
                        productcode = productcode.replace('#', '')
                       
                        tabel = html.find('tbody')
                        tabelrow = tabel.find_all('tr')
                        stock = tabel.find_all('td', class_='text-center')

                    except AttributeError as e:
                        pass
                    except IndexError as e:
                        pass
                
                    try:
                        if stock is not None:
                            size = []
                            Stok_Size = []
                            title = []
                            skuid = []
                            price = []
   
                            for st in tabelrow:
                                Size = st.find('td').strong.contents[0].replace('Size ','')
                                Price = st.find('span', class_='price-maroon').text.strip().strip('\n').replace('.','').replace('Rp ','')
                                stok = st.find('td', class_='text-center').text.strip().strip('\n').replace('pcs','').replace('Habis','0')
                                
                                title.append(judul)
                                skuid.append(productcode)
                                size.append(Size)
                                Stok_Size.append(stok)
                                price.append(Price)

                            temp_df = pd.DataFrame({
                                'PRODUCT NAME' : title, 
                                'PRODUCT CODE' : skuid, 
                                'SIZE' :size, 
                                'STOCK' : Stok_Size, 
                                'PRICE' : price
                                })
                            results_df = results_df.append(temp_df).reset_index(drop=True) #<-- dumping that data into a results dataframe
                            results_df.to_csv('Hasil Cek Stock JSK Jeans '+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv', index=False, encoding="utf-8")#<-- writing the results dataframe to csv

                        else:
                            pass
            
                    except IndexError:
                        pass
                    finally:
                        pass
    
    def scrape(self, widgets, cookies):
        os.chdir('..........')
        results_df = pd.DataFrame() #<-- initialize a results dataframe to dump/store the data you collect after each iteration
        with open('URL Order JSK Jeans Pria & Wanita_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv','r') as f:
        #with open('URL Order JSK Jeans_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv','r') as f:
            urllist = csv.reader(f, delimiter=',')

            skipheader = next(urllist)#start loop from seconds row
            # print('\n' + str(skipheader))

            lines = list(urllist)
            print('\nTotal produk pria & wanita ' + str(len(lines))+ ' produk\n\n')
            loading = ['\x1b[32mGet scrape from '+str(len(lines))+' Products\x1b[39m']
            with progressbar.ProgressBar(widgets=loading + widgets, max_value=len(lines)) as bar:
                for row in enumerate(lines,1):
                    data = []
                    index = row[0]
                    lis = row[1]
                    url = lis[2]
                    bar.update(index)
            
                    try:
                        r = requests.get(url, cookies=cookies)
                        html = BeautifulSoup(r.content, 'html.parser')

                        formstok = html.find('div', class_='tab-pane active')
                        description = html.find('span', class_='desccontent').text.rsplit('Harga Jual', 1)[0]
                        description = description.replace('                                    ','')
                        description = description.replace('                            ','')
                        description = description.replace('\n\n\n','')

                        ttl = formstok.find('h5', class_='mv').strong.contents[0]
                        pc = formstok.find('h5', class_='mv').strong.contents[2]
                        judul = ttl.replace('\n                                ','')
                        productcode = pc.replace('\n','')
                        productcode = productcode.replace('   ', '#')
                        productcode = productcode.replace('  ', '#')
                        productcode = productcode.replace('# ', '')
                        productcode = productcode.replace('#', '')
                       
                        tabel = html.find('tbody')
                        tabelrow = tabel.find_all('tr')
                        td = html.find_all('tbody')#, class_='text-center'
                        for i in td:
                            weight = i.find('td', class_="text-center").text.replace('\n', '')
                            weight= weight.replace('                                                                                                                        ', '')
                            weight = weight.replace('\n', '_')


                        stock = tabel.find_all('td', class_='text-center')

                        carousel = html.find('div', class_='carousel-inner')
                        img = carousel.find_all('img', class_='img-responsive')

                        foto = []
                        for i in img:
                            urlimage = i.get('src')
                            foto.append('https:/www.jskjeans.co.id'+ urlimage)
                            

                        if stock:
                            varian =[]
                            for st in tabelrow:
                                Size = st.find('td').strong.contents[0].replace('Size ','')
                                Price = st.find('span', class_='price-maroon').text.strip().strip('\n').replace('.','').replace('Rp ','')
                                stok = st.find('td', class_='text-center').text.strip().strip('\n').replace('pcs','').replace('Habis','0')
                                varian.append(Size +"_"+ Price +"_" + stok)    
                        else:
                            ''

                        #Save to CSV
                        data.append({

                            '(A) Produk ID JSK Jeans'       :productcode,
                            '(B) Nama Produk'               :judul,
                            '(C) Berat Produk'              :weight,
                            '(D) Varian Produk'             :varian,
                            '(E) Deskripsi'                 :description,
                            '(F) URL Produk'                :foto,
                        })


                        temp_df = pd.DataFrame(data) #<-- temporary storing the data in a dataframe
                        results_df = results_df.append(temp_df).reset_index(drop=True) #<-- dumping that data into a results dataframe
                        results_df.to_csv('Result Scrape JSK Jeans_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'_.csv', index=False, encoding="utf-8")#columns=col, <-- writing the results dataframe to csv
                        
                        # testing = pd.read_csv('Result Scrape JSK Jeans_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.csv')
                        # heading = testing.head(1000)
                        # discription = testing.describe()
                        # print(heading, end='')
            
                    except UnboundLocalError as ULE:
                        # pass
                        print ('Baris ke ', index, 'url :', url, ULE)
             
                    except ValueError as ve:
                        # pass
                        print('Baris ke ', index, 'url :', url,ve)
                      
                    except IndexError as idx:
                        # pass
                        print('Baris ke ', index, 'url :', url,idx)
                        
                    except KeyError as key:
                        # pass
                        print('Baris ke ', index, 'url :', url,key)
                        
                    except TypeError as type:
                        # pass
                        print('Baris ke ', index, 'url :', url,type)
                        
                    except AttributeError as att:
                        # pass
                        print('Baris ke ', index, 'url :', url,att)
                    
                    except ConnectionError as Con:
                        # pass
                        print('Baris ke ', index, 'url :', url,Con)

jsk()