from bs4 import BeautifulSoup

path = """
    <div class="slice_body_1">
      <span style="font-size: 60px; color: #ff8400">developer – </span
      ><span style="font-size: 46px; color: #ff8400">software – </span
      ><span style="font-size: 40px; color: #ff8400">engineer – </span
      ><span style="font-size: 32px; color: #ff8400">sheher – </span
      ><span style="font-size: 31px; color: #ff8400">web – </span
      ><span style="font-size: 28px; color: #ff8400">dev – </span
      ><span style="font-size: 22px; color: #ff8400">tech – </span
      ><span style="font-size: 18px; color: #ff8400">javascript – </span
      ><span style="font-size: 17px; color: #ff8400">frontend – </span
      ><span style="font-size: 16px; color: #ff8400">learning – </span
      ><span style="font-size: 15px; color: #ff8400">own – </span
      ><span style="font-size: 15px; color: #ff8400">code – </span
      ><span style="font-size: 13px; color: #ff8400">creator – </span
      ><span style="font-size: 12px; color: #ff8400">hehim – </span
      ><span style="font-size: 12px; color: #ff8400">community – </span
      ><span style="font-size: 11px; color: #ff8400">opinions – </span
      ><span style="font-size: 11px; color: #ff8400">enthusiast – </span
      ><span style="font-size: 11px; color: #ff8400">content – </span
      ><span style="font-size: 10px; color: #ff8400">founder – </span
      ><span style="font-size: 10px; color: #ff8400">building – </span
      ><span style="font-size: 10px; color: #ff8400">gwent – </span
      ><span style="font-size: 10px; color: #ff8400">speaker – </span
      ><span style="font-size: 9px; color: #ff8400">student – </span
      ><span style="font-size: 9px; color: #ff8400">react – </span
      ><span style="font-size: 9px; color: #ff8400">tweets</span>
      <p></p>
      <hr />
      <p></p>
      <b>Two word bio cloud</b>
      <p></p>
      <span style="font-size: 60px; color: #ff8400">software engineer – </span
      ><span style="font-size: 27px; color: #ff8400">web developer – </span
      ><span style="font-size: 21px; color: #ff8400">software developer – </span
      ><span style="font-size: 20px; color: #ff8400">frontend developer – </span
      ><span style="font-size: 19px; color: #ff8400">content creator – </span
      ><span style="font-size: 15px; color: #ff8400">web dev – </span
      ><span style="font-size: 15px; color: #ff8400">full stack – </span
      ><span style="font-size: 10px; color: #ff8400">web development – </span
      ><span style="font-size: 9px; color: #ff8400">html css</span>
    </div>
    """
soup = BeautifulSoup(path, features="lxml").get_text(strip=True
                                                     )  # .find_all("div", {"class": "slice_body_1"})
span = soup.split('–')
print(soup)
