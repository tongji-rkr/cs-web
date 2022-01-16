import os
import sys
import click
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user,login_required, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mov' 

login_manager = LoginManager(app) # 实例化扩展类
login_manager.login_view = 'login'

WIN = sys.platform.startswith('win')
if WIN: # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else: # 否则使用四个斜线
    prefix = 'sqlite:////'

# 配置多个数据库连接
SQLALCHEMY_BINDS = { 
    'test1': 'sqlite:///music.db',
    'test2': 'sqlite:///movie.db',
    'test3': 'sqlite:///comment.db',
    'test4': 'sqlite:///search.db'
}

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
# 在扩展类实例化前加载配置

db = SQLAlchemy(app)
list=['red','orange','yellow','green','blue','purple','grey']

class User(db.Model, UserMixin):
    #__tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # 用户名
    password_hash = db.Column(db.String(128)) # 密码散列值
    def set_password(self, password): # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password) #将生成的密码保持到对应字段
    def validate_password(self, password): # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)
# 返回布尔值
class Music(db.Model): # 表名将会是 music
    #__tablename__= 'music'
    __bind_key__ = 'test1' # 已设置__bind_key__,则采用设置的数据库引擎　　
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(60)) # 歌手名称
    photo= db.Column(db.String(60)) # 歌手图片
    intro= db.Column(db.String(1000)) #歌手简介
    #color= db.Column(db.String(10)) #背景颜色
class Movie(db.Model): # 表名将会是 movie
    #__tablename__='movie'
    __bind_key__ = 'test2' # 已设置__bind_key__,则采用设置的数据库引擎　　
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(60)) # 电影名称
    photo= db.Column(db.String(60)) # 歌手图片
    intro= db.Column(db.String(1000)) #歌手简介
    year=db.Column(db.String(4)) #电影年份
    #color= db.Column(db.String(10)) #背景颜色
class Comment(db.Model): # 表名将会是 comment
    #__tablename__='commment'
    __bind_key__ = 'test3' # 已设置__bind_key__,则采用设置的数据库引擎　　
    id = db.Column(db.Integer, primary_key=True) # 主键
    name= db.Column(db.String(60)) #评论的电影
    score= db.Column(db.String(60)) #评论的分数
    year=db.Column(db.String(4)) #评论时间年数
    month=db.Column(db.String(2)) #评论时间月数
    day=db.Column(db.String(2)) #评论时间日数
    cmt=db.Column(db.String(1000)) #评论
class Search(db.Model): # 表名将会是 search
    #__tablename__='search'
    __bind_key__ = 'test4' # 已设置__bind_key__,则采用设置的数据库引擎　　
    id = db.Column(db.Integer, primary_key=True) # 主键
    content = db.Column(db.String(60)) # 搜索内容

@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'RKR'
    musics = [
        {'name': '周杰伦', 'photo': 'images/1.png','intro': '周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，祖籍福建省泉州市永春县，中国台湾流行乐男歌手、原创音乐人、演员、导演、编剧，毕业于淡江中学。 2000年发行首张个人专辑《Jay》。2001年发行的专辑《范特西》奠定其融合中西方音乐的风格。2002年举行“The One”世界巡回演唱会。2003年成为美国《时代周刊》封面人物。2004年获得世界音乐大奖中国区最畅销艺人奖。2005年凭借动作片《头文字D》获得台湾电影金马奖、香港电影金像奖最佳新人奖。2006年起连续三年获得世界音乐大奖中国区最畅销艺人奖。2007年自编自导的文艺片《不能说的秘密》获得台湾电影金马奖年度台湾杰出电影奖。 2008年凭借歌曲《青花瓷》获得第19届金曲奖最佳作曲人奖。2009年入选美国CNN评出的“25位亚洲最具影响力的人物”，同年获得第20届金曲奖最佳国语男歌手奖。2010年入选美国《Fast Company》评出的“全球百大创意人物”。2011年再度获得金曲奖最佳国语男歌手奖，并且第4次获得金曲奖最佳国语专辑奖；同年主演好莱坞电影《青蜂侠》。2012年登福布斯中国名人榜榜首。2014年发行华语乐坛首张数字音乐专辑《哎呦，不错哦》。2019年起举行“嘉年华”世界巡回演唱会。 演艺事业外，他还涉足商业、设计等领域。2007年成立杰威尔有限公司。2011年担任华硕笔电设计师并入股香港文化传信集团。 周杰伦热心公益慈善，多次向中国内地灾区捐款捐物。2008年捐款援建希望小学。2014年担任中国禁毒宣传形象大使。'},
        {'name': '林俊杰', 'photo': 'images/2.png','intro': 'JJ林俊杰的创作来自最深的情感，他的声音唱出灵魂的璀璨，他把音乐和梦想当做能量，一路走到无人取代的地位，他写下华语乐坛最动人的经典乐章，撼动亚洲数十亿颗心跳。他是亚洲乐坛全能唱作天王 JJ 林俊杰。 2003年首发第一张个人创作专辑《乐行者》，取得不俗成绩；其杰出的创作才能又在之后2004年的凭借歌曲【江南】而成名，并于同年获得第15届金曲奖之「最佳演唱新人奖」。随后的【小酒窝】、【曹操】、【她说】等歌曲亦造成广大回响。2011年8月8日携手华纳，迈出世界。 2020至2021年【幸存者·如你】双维度EP，创造全新音乐视角。由JJ 林俊杰亲自领导整张专辑的企划创意与视觉，新专辑一推出便占据大中华区各大排行榜，销售量更在一个月内突破百万。 把音乐和梦想当做能量，一路走到无人取代的地位，写下华语乐坛最动人的经典乐章，他是亚洲全能唱作天王JJ林俊杰。'},
        {'name': '邓紫棋', 'photo': 'images/3.png','intro': '邓紫棋（G.E.M.），本名邓诗颖，1991年8月16日出生于上海市，中国香港流行乐女歌手、词曲作者、音乐制作人。 2008年，发行个人首张音乐EP《G.E.M.》，凭该EP获得香港叱咤乐坛流行榜“叱咤乐坛生力军女歌手（金奖）”。2009年，发行个人首张音乐专辑《18...》。2011年，成为首位登上香港体育馆开唱的90后华语女歌手。2012年，凭借音乐专辑《Xposed》入围第24届台湾金曲奖“最佳国语女歌手奖”，并获得IFPI香港唱片销量大奖“全年最高销量女歌手奖”和“最高销量国语唱片奖”。2013年，举行邓紫棋“X.X.X.”世界巡回演唱会。2014年，获得湖南卫视歌唱真人秀节目《我是歌手第二季》总决赛亚军；同年，获得第27届美国儿童选择奖“最受欢迎亚洲艺人奖”。 2015年，登上2015年中央电视台春节联欢晚会，弹唱歌曲《多远都要在一起》；同年，位列《2015年福布斯中国名人榜》第11名。2016年，入选福布斯《全球30岁以下最具潜力音乐人榜单》；同年，获得MTV欧洲音乐奖“中国内地及香港地区最佳艺人奖”。2018年，成为美国国家航空航天局“科学突破奖”首位亚洲颁奖女艺人；同年，入选英国广播公司BBC发布的《全球最具影响力百大女性榜单》。2019年，《光年之外》MV在视频平台YouTube突破2亿次点击量。2020年，凭借音乐专辑《摩天动物园》获得第31届台湾金曲奖“评审团奖”；同年，获得Mnet亚洲音乐大奖“最佳亚洲艺人奖”。'},
        {'name': '李荣浩', 'photo': 'images/4.png','intro': '李荣浩（Ronghao Li），1985年7月11日出生于安徽省蚌埠市，中国内地流行乐男歌手、词曲创作人、音乐制作人、演员。 2010年，发行首张个人音乐EP《小黄》。2013年，发行个人首张音乐专辑《模特》，凭该专辑成为首位获得台湾金曲奖“最佳新人奖”的中国大陆歌手。2014年，发行个人同名音乐专辑《李荣浩》，凭该专辑获得中国TOP排行榜内地年度最佳男歌手奖。2016年，发行个人音乐专辑《有理想》，随后，举行的23场“有理想”世界巡演获得第21届华语榜中榜亚洲影响力最佳演唱会奖。2017年，发行个人音乐专辑《嗯》，凭该专辑获得第22届全球华语榜中榜亚洲影响力最佳男歌手奖；同年，他的个人巡演首次登陆香港红磡体育馆和台北小巨蛋体育馆。2018年，发行个人音乐专辑《耳朵》，凭该专辑提名第30届台湾金曲奖最佳国语男歌手奖。2019年，担任浙江卫视歌唱选秀节目《中国好声音》的导师；同年，获得Mnet亚洲音乐大奖亚洲最佳艺人奖。2020年，发行音乐专辑《麻雀》。2021年，发行专辑《不遗憾》。'},
        {'name': 'Beyond', 'photo': 'images/5.png','intro': 'Beyond，中国香港摇滚乐队，成立于1983年，由黄家驹、黄贯中、黄家强、叶世荣组成。 1983年参加“山叶吉他比赛”获得冠军并正式出道。1986年自资发行乐队首张专辑《再见理想》。1988年凭借粤语专辑《秘密警察》在香港乐坛获得关注；同年凭借歌曲《大地》获得十大劲歌金曲奖。1989年凭借歌曲《真的爱你》获得十大中文金曲奖、十大劲歌金曲奖。1990年凭借歌曲《光辉岁月》获得十大劲歌金曲奖。1991年主演电影《Beyond日记之莫欺少年穷》；同年9月在香港红磡体育馆举办“Beyond Live 1991 生命接触演唱会”。1992年赴日本发展演艺事业。1993年凭借粤语专辑《乐与怒》中的歌曲《海阔天空》获得十大中文金曲奖；6月30日，黄家驹去世，乐队以三名成员的组成形式继续发展。 1994年发行专辑《二楼后座》。1995年至1999年发行的《Sound》《请将手放开》《不见不散》等五张专辑标志着乐队音乐风格的转变。1996年起连续四年获得叱咤乐坛流行榜叱咤乐坛组合金奖。1999年乐队宣布暂时解散。2002年获得第25届十大中文金曲金曲银禧荣誉大奖。2003年正式复出乐坛，并举办“Beyond超越Beyond”世界巡回演唱会。2004年凭借歌曲《长空》获得香港电影金像奖最佳原创电影歌曲奖。2005年举行“Beyond The Story Live 2005”世界巡回告别演唱会；同年乐队正式解散。2010年获得华语金曲奖“30年经典评选”的全部奖项 。 演艺事业外，Beyond热心公益慈善。1991年前往非洲探访第三世界的穷困人民，并成立第三世界基金。'},
        {'name': '泰勒·斯威夫特', 'photo': 'images/6.png','intro': '泰勒·斯威夫特（Taylor Swift），1989年12月13日出生于美国宾夕法尼亚州雷丁，美国著名女歌手、词曲作者、音乐制作人、演员。 2006年，Taylor发行个人首张录音室专辑《Taylor Swift》，该专辑获得美国唱片业协会认证5倍白金唱片销量。2008年，发行第二张个人录音室专辑《Fearless》，该专辑在美国公告牌专辑榜上获11周冠军，于2020年被认证钻石唱片销量，并获得第52届格莱美奖年度专辑奖。2010年，Taylor发行第三张个人录音室专辑《Speak Now》，单曲《Mean》获2座格莱美奖。同年，获创作人名人堂“哈尔·大卫星光大奖” 。2011年，凭借三张实体专辑销量，获得中国区“五白金唱片”销量认证。2012年，，并发行音乐专辑《Red》，该专辑实体版本获得中国区“双白金唱片”销量认证。2013年，获得第47届乡村音乐协会奖巅峰奖。2014年，Taylor开始向流行乐歌手转型并发行第五张个人录音室专辑《1989》，该专辑获得第58届格莱美奖年度专辑奖，国际唱片业协会（IFPI）宣布该专辑为“年度全球唱片销量冠军” 。同年，获得全美音乐奖迪克·克拉克终身成就奖，并入围《时代周刊（美国版）》年度人物。目前，Taylor在公告牌上拥有9张冠军专辑，登顶周数共51周，成为历史上专辑登顶周数最多的女艺人！2021年5月，Taylor Swift拿下全英音乐奖全球偶像大奖，成为历史上首个非英国歌手和首位女性获得该奖项。同月，Taylor Swift被公告牌官方评为2010s年代艺人第二名，也是所有女艺人中的第一名。'},
        {'name': 'EGOIST', 'photo': 'images/7.png','intro': 'EGOIST是在2011年10月TV动画《罪恶王冠》中设定的拥有超高人气及超大影响力的的网络歌手，在剧中演唱OP/ED以及插曲。而实际上这位歌手则是由supercell的ryo担任制作、并由ryo选出的chelly担任演唱的角色。在该动画结束后仍继续以团体名称活跃，所属唱片公司为SACRA MUSIC。'},
        {'name': 'Aimer', 'photo': 'images/8.png','intro': 'Aimer是一名日本女歌手，于2020年公布个人资料，生日为1990年7月9日。艺名Aimer取自法语，意为“爱”，作词以aimerrhythm名义。在2011年以单曲《六等星の夜/悲しみはオーロラに/TWINKLE TWINKLE LITTLE STAR》正式出道，隶属的唱片公司是日本索尼音乐娱乐旗下的SME Records。所属的经纪公司是FOURseam。'},
        {'name': '贾斯汀·比伯', 'photo': 'images/9.png','intro': '贾斯汀·比伯（Justin Bieber），1994年3月1日出生于加拿大安大略省斯特拉特福市，加拿大流行乐男歌手、影视演员。 2008年，贾斯汀·比伯在视频网站YouTube上被其经纪人斯科特发现，随后被亚瑟小子培养进入歌坛。2009年11月17日，发行第一张个人专辑《My World》。2010年3月，第二张个人专辑《My World2.0》发行一周便登上了公告牌专辑冠军，并且该专辑获得2010全美音乐奖最佳专辑奖 。11月，凭借单曲《Baby》获得第27届MTV音乐奖最佳新人。2011年8月，凭借歌曲《U Smile》获得第28届MTV音乐录影带大奖最佳男歌手录影带奖。11月，获得欧洲MTV音乐奖最佳流行歌手奖和最佳男歌手奖。2012年7月，凭借单曲《Boyfriend》获得美国青少年选择奖最佳男歌手。2013年，发行现场专辑《Believe Acoustic》，并凭借该专辑获得了第40届全美音乐奖最佳艺人奖。2015年8月，发行个人单曲《What Do You Mean?》并获得公告牌百强单曲榜首周冠军 。11月，发行个人专辑《Purpose》，该专辑被提名第57届格莱美奖的年度专辑奖项。2016年2月，凭借歌曲《Where Are U Now》夺得第58届格莱美最佳舞曲录制奖。7月，演唱的歌曲《Sorry》提名美国MTV音乐录影带大奖年度最佳录影带 。12月，单曲《Love Yourself》获得第59届格莱美奖年度歌曲提名。2017年8月17日，与BloodPop联合发布单曲《Friends》。2020年2月14日，发布录音室专辑《Changes》。2021年3月26日推出专辑《Justice》。'},
        {'name': '筷子兄弟', 'photo': 'images/10.png','intro': '筷子兄弟，中国内地影视歌三栖组合，由肖央、王太利组成。 2007年，筷子兄弟成军；同年二人主演音乐电影《男艺伎回忆录》在猫扑网首发，演唱歌曲《祝福你亲爱的》在网络走红。2010年10月28日，筷子兄弟自编自导自演的11度青春系列电影之《老男孩》上映，并为该电影演唱同名歌曲《老男孩》。2011年12月21日携手中国视频网站优酷感恩呈现最新力作《父亲》于12月21日全国首映，并为电影献唱同名歌曲，获得“全球华语榜中榜”首届主题盛典——2012“华语咪咕榜中榜励志金曲·成都盛典”获得感恩励志金曲奖“与首届“金微奖”之最佳微电影奖。 2014年5月推出歌曲《小苹果》走红，主演电影《老男孩之猛龙过江》于7月10日上映；同年11月23日受“第42届全美音乐奖”主办方邀请，担任表演嘉宾，成为首个登上全美音乐奖舞台的华语艺人组合，并凭借歌曲《小苹果》获得“年度最佳国际流行音乐奖”。 2015年1月8日凭借歌曲《小苹果》获得第十四届华鼎奖华语年度最受欢迎单曲与华语年度最受欢迎组合两个奖项；同年2月18日登上央视春晚舞台，与凤凰传奇及北京群众艺术馆共同表演作品《最炫小苹果》。'}
    ]
    movies=[
        {'name': '怪物史莱克', 'photo': 'images/11.png','intro': '很久很久以前，在一个遥远的大沼泽里，住着一只叫史莱克的绿色怪物，过着悠闲的生活。有一天，他平静的生活被几个不速之客打破，它们是一只眼神不怎么好的小老鼠，一只大坏狼和三只无家可归的小猪，他们都是从童话王国里逃出来的，史莱克为了让他们远离自己沼泽地，还自己以清净，就让一个会说话的驴子带路，去了那个王国找国王。此时 国王正在为自己王位发愁，因为魔镜告诉他要娶个公主才能真正成为国王，所以他选定了困在高塔之上，有火龙守护的公主菲奥娜，并且准备选拔骑士去解救公主。正好史莱克赶来，打败了所有骑士，国王本要抓史莱克，后来将计就计，让史莱克去救公主，条件是还回史莱克的沼泽地，于是，他和驴子上路了。史莱克成功的救出公主，但在途中发现自己爱上了公主菲奥娜，而公主也已经对史莱克有了感情，但是由于公主自身被诅咒，白天有着美丽的外貌，而晚上会变成怪物，所以一直不敢表白。但最后真爱战胜了外貌，公主最终和史莱克在一起。','year':'2001'},
        {'name': '速度与激情', 'photo': 'images/12.png','intro': '洛杉矶的年轻人都热衷于街头赛车，在这里，只要你拥有速度，你就拥有一切。新晋警官布赖恩（保罗·沃克 Paul Walker 饰）为了破获最近屡屡发生的飞车党劫车案而充当卧底，打入这里活跃的飞车党帮派中，搜集证据以期将罪犯绳之以法。布赖恩凭借高超的车技很快赢得了飞车党老大多米尼克（范·迪塞尔 Vin Diesel 饰）的欣赏和信任，并且很快和多米尼克的妹妹米亚（乔丹娜·布鲁斯特 Jordana Brewster 饰）堕入爱河。然而飞车党的第二把手文斯却对布赖恩充满敌意。原来文斯一直暗恋米亚，而且布赖恩的到来威胁着他二把手的地位。这时，飞车党的党员们开始怀疑他们内部藏有奸细，布赖恩的日子开始不好过。而且和多米尼克接触越久，他们之间的友谊就越加深厚，布赖恩开始进退两难。','year':'2011'},
        {'name': '暮光之城', 'photo': 'images/13.png','intro': '在美国一个名叫福克斯的地方，住着一位英俊帅气的男青年爱德华。他出没神秘，与世无争，他的家人同样低调神秘，原因在于他是一只永远不会衰老，更不会死亡的吸血鬼。爱德华生于20世纪的第一年，自从1918年发育成长为十七岁的翩翩少年之后，他便再也没有衰老，永远保持着年轻俊朗的外形。时光飞梭，过了近百年后，他已经不再靠吸人血为生，因为爱德华和同是吸血鬼的家人都秉持着素食主义，只吸食动物的血。十七岁的少女伊莎贝拉从小与母亲相依为命，因为父母的感情破裂，母亲带着她去了另一个城市。但当她长大的时候，母亲却决定再婚，由于继父是位棒球运动员，需要来回奔波，伊莎贝拉回到在福克斯的父亲查理的身边。在学校里，她结识了男孩爱德华，很快就被爱德华魅力所吸引，并渐渐喜欢上了他。不过爱德华虽然也喜欢伊莎贝拉，可是他却深知，一只吸血鬼是没有办法和人类正常生活在一起的。但他又无法忘却伊莎贝拉，也不忍心远走高飞，与伊莎贝拉断绝音信。而这时候另一派吸食人血的吸血鬼来到此地，并无意中盯上了伊莎贝拉，爱德华保护好了伊莎贝拉，两人的感情得到了稳定地发展。','year':'2009'},
        {'name': '复仇者联盟', 'photo': 'images/14.png','intro': '一股突如其来的强大力量从宇宙魔方中出现，还带来了邪神洛基（汤姆·希德勒斯顿饰），他带走了宇宙魔方，并摧毁了实验现场，使长期致力于保护全球安危的“神盾局”感到措手不及。指挥官“独眼侠”尼克·弗瑞（塞缪尔·L·杰克逊饰）意识到他必须创建一个“史上最强”的联盟组织，集结各方超级英雄，才能拯救世界。于是由六大超级英雄－“钢铁侠”托尼·史塔克（小罗伯特·唐尼饰）、“雷神”索尔·奥丁森（克里斯·海姆斯沃斯饰）、“美国队长”史蒂夫·罗杰斯（克里斯·埃文斯饰）、“绿巨人”布鲁斯·班纳（马克·鲁法洛饰）、“黑寡妇”娜塔莎·罗曼诺夫（斯嘉丽·约翰逊饰）和“鹰眼”克林特·巴顿（杰瑞米·雷纳饰）组成的“复仇者联盟”应运而生。他们各显神通，团结一心，终于战胜了来自外星的邪恶势力，保护了地球的安全。','year':'2012'},
        {'name': '加勒比海盗', 'photo': 'images/15.png','intro': '杰克·斯帕罗（约翰尼·德普饰）是个加勒比沿海小镇子上不务正业的小痞子，别看他眼下是混得这么惨，但是当初，他也曾经是一位驾着自己的爱船，率领着众多喽罗纵横海上劫富济贫的侠盗，可惜一个不小心，着了坏蛋船长巴博萨（杰弗瑞·拉什饰）的道儿，被他抢走了心爱的海盗船“黑珍珠号”不说，也让从小立志成为一名出色海盗的杰克倍受打击，心灰意冷的他干脆落拓到这个不起眼的小镇子上混起了日子。某天，当地地方官漂亮动人却又野性难驯的女儿伊丽莎白（凯拉·奈特利饰）被突然冒出来的巴博萨船长领军的一票海盗给劫走了，原来，巴博萨自从从杰克手里抢走了“黑珍珠号”以后，他和手下人就全部中了一个古老的诅咒，每当有月光照在他们身上，他们就会变成一帮半人不鬼的活动骷髅，当海盗再逍遥再自在，背着这么个诅咒过一辈子也郁闷痛苦啊。恰就在这时，巴博萨船长偶然看到了伊丽莎白身上佩带的一个徽章，根据书上记载，它似乎正是解除这个咒语的关键所在，于是一不做二不休，索性连人带东西一起掠上船带走。伊丽莎白被海盗抢走了。这个消息可急坏了和伊丽莎白青梅竹马的铁匠威尔·特纳（奥兰多·布鲁姆饰），万般无奈之下，他只得求助于有过海盗背景的杰克，当杰克知道抢走伊丽莎白的正是和他不共戴天的巴博萨船长时，他立刻答应和威尔一起追踪“黑珍珠号”，为了救美，更为了夺回自己的爱船，于是两人跑去偷了一艘号称是英国舰队最快的帆船，升帆扬旗，和巴博萨船长在美丽而危险的加勒比海上展开了一场惊心动魄的追逐。 [1]','year':'2002'},
        {'name': '盗梦空间', 'photo': 'images/16.png','intro': '多姆·柯布（莱昂纳多·迪卡普里奥饰演）是一位经验老道的窃贼，他在这一行中算得上是最厉害的，因为他能够潜入人们精神最为脆弱的梦境中，窃取潜意识中有价值的秘密。柯布这一罕见的技能使他成为危险的企业间谍活动中最令人垂涎的对象，但这也让他成为了一名国际逃犯，失去自己的所爱。如今柯布有了一个赎罪的机会，只要完成最后一项任务他的生活就会回复本来面目。与以往不同的是，柯布和他的团队这一次的任务不是窃取思想，而是植入思想。如果他们成功，这就是一次完美犯罪。但是即使提前做好了细致专业的安排，也无法预料到危险的敌人对他们的行动早已了如指掌，而只有柯布能够预料到敌人的行踪。','year':'2010'},
        {'name': '碟中谍', 'photo': 'images/17.png','intro': '中情局向以吉姆为首的特工小组发来指令，一名特工人员已经叛国，将在布拉格的领事馆窃取中情局在东欧潜伏的特工名单，一旦落入坏人手中，后果将不堪设想。他们奉命获取该特工窃取情报的证据，并将其与买家逮捕。很快，在吉姆的策划下，一线主力伊森·亨特和其他几名成员全部到位，不过当计划进行到一半时，情况突然急转直下，包括吉姆在内的小组成员相继殒命，情报失踪，只有伊森一人生还。精神几乎崩溃的伊森与上司见面，却因幸免遇难和帐户上突然多出的12万美元被指认为叛徒，原来失窃的是假情报，行动的真正目的是为了查出内奸。突出重围的伊森决定查出叛徒，而此时，同样侥幸生还的吉姆的妻子克莱尔与伊森重逢。同买家麦克斯取得联系后，伊森承诺自己能够弄到特工名单，条件除了1000万美元外，还要其交出内奸。伊森找到中情局的两名停职特工，一行四人潜入兰利总部，成功窃取情报。赶到伦敦的伊森突然邂逅吉姆，在吉姆的谎言下，伊森逐渐理清脉络，吉姆和克莱尔应该是幕后真凶。不久，伊森、麦克斯、吉姆和中情局齐聚交易情报的火车，展开殊死搏斗。一番惊心动魄的交锋过后，伊森终于铲除内奸，重新回到特工行列。','year':'1996'},
        {'name': '唐人街探案', 'photo': 'images/18.png','intro': '天赋异禀的结巴少年“秦风”警校落榜，被姥姥遣送泰国找远房表舅——号称“唐人街第一神探 ”，实则“猥琐”大叔的“唐仁“散心。不想一夜花天酒地后，唐仁沦为离奇凶案嫌疑人，不得不和秦风亡命天涯，穷追不舍的警探——-“疯狗”黄兰登；无敌幸运的警察——“草包”坤泰；穷凶极恶、阴差阳错的“匪帮三人组”；高深莫测的“唐人街教父”；“美艳风骚老板娘”等悉数登场。七天，唐仁、秦风这对“欢喜冤家”、“天作之合”必须取长补短、同仇敌忾，他们要在躲避警察追捕、匪帮追杀、黑帮围剿的同时，在短短“七天”内，完成找到“失落的黄金”、查明“真凶”、为他们“洗清罪名”这些“逆天”的任务。','year':'2015'},
        {'name': '毒液', 'photo': 'images/19.png','intro': '身为记者的埃迪·布洛克（汤姆·哈迪饰）在调查生命基金会老板卡尔顿·德雷克（里兹·阿迈德饰）的过程中，事业遭受重创，与未婚妻安妮·韦英（米歇尔·威廉姆斯饰）的关系岌岌可危，并意外被外星共生体控制，他历经挣扎对抗，最终成为拥有强大超能力，无人可挡的“毒液” 。','year':'2018'},
        {'name': '神奇女侠', 'photo': 'images/20.png','intro': '戴安娜·普林斯（盖尔·加朵饰）生活在亚马逊天堂岛，岛上只有女性，作为众神之王宙斯与亚马逊女王希波吕忒（康妮·尼尔森饰）的女儿，在她的成长过程中，一直受到母亲和姨母安提俄珀（罗宾·怀特饰）的悉心呵护。直到有一天，一架战机坠入天堂岛附近海域，戴安娜的平静生活由此被打破。戴安娜将坠海的飞行员史蒂夫·特雷弗（克里斯·派恩饰）救起，但其母亲对这位普通男人的世界没有一点兴趣。史蒂夫强调自己的目标是结束第一次世界大战，而戴安娜则认为这场人类的浩劫或许是战神阿瑞斯捣的鬼，于是决定与史蒂夫一起前往战争前线，第一次亲身体验到了人类战争的威力，并逐渐理解了身为英雄的意义和代价','year':'2017'}
    ]
    comments=[
        {'name': '管理员', 'score': '5','year': '2021','month': '11','day': '7','cmt': '这是第一条评论'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in musics:
        music = Music(name=m['name'],photo=m['photo'],intro=m['intro'])
        db.session.add(music)
        db.session.commit()
    for m in movies:
        movie = Movie(name=m['name'],photo=m['photo'],intro=m['intro'],year=m['year'])
        db.session.add(movie)
        db.session.commit()
    for m in comments:
        comment = Comment(name=m['name'],score=m['score'],year=m['year'],month=m['month'],day=m['day'],cmt=m['cmt'])
        db.session.add(comment)
        db.session.commit()
    click.echo('Done.')

@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    hide_input=False
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password) # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password) # 设置密码
        db.session.add(user)
    db.session.commit() # 提交数据库会话
    click.echo('Done.')

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
    return user # 返回用户对象

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user) # 登入用户
            flash('Login success.')
            return redirect(url_for('index')) # 重定向到主页
        flash('Invalid username or password.') # 如果验证失败，显示错误消息
        return redirect(url_for('login')) # 重定向回登录页面
    return render_template('login.html')

@app.route('/logout')
@login_required # 用于视图保护，后面会详细介绍
def logout():
    logout_user() # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index')) # 重定向回首页

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()  
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')


@app.route('/music/edit1/<int:music_id>', methods=['GET', 'POST'])
@login_required
def edit1(music_id):
    music = Music.query.get_or_404(music_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        intro = request.form['intro']
        if not intro or len(intro)> 1000:
            flash('Invalid input.')
            return redirect(url_for('edit1', music_id=music.id))
        # 重定向回对应的编辑页面
        music.intro = intro # 更新歌手/组合简介
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('music')) # 重定向回music页面
    return render_template('edit1.html', music=music) # 传入被编辑的音乐

@app.route('/movie/edit2/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit2(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # 处理编辑表单的提交请求
        intro = request.form['intro']
        year = request.form['year']
        if not intro or not year or len(year) > 4 or len(intro)> 1000:
            flash('Invalid input.')
            return redirect(url_for('edit2', movie_id=movie.id))
        # 重定向回对应的编辑页面
        movie.intro = intro # 更新电影名称
        movie.year = year # 更新年份
        db.session.commit() # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('movie')) # 重定向回movie页面
    return render_template('edit2.html', movie=movie) # 传入被编辑的电影记录

@app.route('/music/detail1/<int:music_id>', methods=['GET', 'POST'])
def detail1(music_id):
    music = Music.query.get_or_404(music_id)
    return render_template('detail1.html', music=music) # 传入被编辑的音乐

@app.route('/music/detail2/<int:movie_id>', methods=['GET', 'POST'])
def detail2(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('detail2.html', movie=movie) # 传入被编辑的音乐

@app.route('/music/delete/<int:music_id>', methods=['POST'])
@login_required # 登录保护
def delete1(music_id):
    music = Music.query.get_or_404(music_id)
    db.session.delete(music)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('music'))

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required # 登录保护
def delete2(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('movie'))

@app.route('/comment/delete/<int:comment_id>', methods=['POST'])
@login_required # 登录保护
def delete3(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('comment'))

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/search', methods=['GET', 'POST'])
def search():
    content=request.args.get('content')
    user=User.query.first()
    musics1=Music.query.filter(Music.name==content).all()
    movies1=Movie.query.filter(Movie.name==content).all()
    movies2=Movie.query.filter(Movie.year==content).all()
    return render_template('search.html', user=user, musics=musics1,movies1=movies1,movies2=movies2,content=content)


@app.route('/music', methods=['GET', 'POST'])
def music():
    if request.method == 'POST': # 判断是否是 POST 请求
        # 获取表单数据
        if not current_user.is_authenticated: # 如果当前用户未认证
            return redirect(url_for('index')) # 重定向到主页
        name = request.form.get('name') # 传入表单对应输入字段的name 值
        photo = request.form.get('photo') # 传入表单对应输入字段的name 值
        intro = request.form.get('intro')
        if not name or not photo or not intro or len(name) > 60 or len(photo)> 60 or len(intro)> 1000:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('music')) # 重定向回主页
        # 保存表单数据到数据库
        music = Music(name=name,photo=photo,intro=intro) # 创建记录
        db.session.add(music) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('music')) # 重定向回主页
    user = User.query.first()
    musics = Music.query.all()
    return render_template('music.html', user=user, musics=musics)

@app.route('/movie', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST': # 判断是否是 POST 请求
        # 获取表单数据
        if not current_user.is_authenticated: # 如果当前用户未认证
            return redirect(url_for('index')) # 重定向到主页
        name = request.form.get('name') # 传入表单对应输入字段的name 值
        photo = request.form.get('photo') # 传入表单对应输入字段的name 值
        intro = request.form.get('intro')
        year = request.form.get('year')
        # 验证数据
        if not name or not photo or not intro or not year or len(year)>4 or len(name) > 60 or len(photo)> 60 or len(intro)> 1000:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('movie')) # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(name=name, photo=photo,intro=intro,year=year) # 创建记录
        db.session.add(movie) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('movie')) # 重定向回主页
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('movie.html', user=user, movies=movies)

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    user = User.query.first()
    if request.method == 'POST': # 判断是否是 POST 请求
        # 获取表单数据
        name = request.form.get('name') 
        score =request.form.get('score')
        current_time=datetime.datetime.now()
        year = current_time.strftime('%Y')
        month = current_time.strftime('%m')
        day = current_time.strftime('%d')
        cmt = request.form.get('cmt')
        # 验证数据
        if not name or not score or not cmt or len(cmt) > 1000 or len(score)>2 or len(name)> 60:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('comment')) # 重定向回主页
        # 保存表单数据到数据库
        comment = Comment(name=name, score=score, year=year,month=month,day=day,cmt=cmt) # 创建记录
        db.session.add(comment) # 添加到数据库会话
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示
        return redirect(url_for('comment')) # 重定向回主页

    comments = Comment.query.all()
    return render_template('comment.html', user=user, comments=comments)   

@app.route('/', methods=['GET', 'POST'])
def index():
    user = User.query.first()
    music=Music.query.first()
    movie=Movie.query.first()
    comment=Comment.query.first()
    return render_template('index.html', user=user,music=music,movie=movie,comment=comment)