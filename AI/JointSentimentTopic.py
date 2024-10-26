import numpy as np
import random
import tqdm
import pandas as pd 

# JST algorithm
class JST:

    def __init__(self, docs, K, S, alpha, beta, gamma, iterations, paradigm_pos, paradigm_neg):

        self.docs = docs  # 문서 집합(corpus)

        self.V  =len(set(word for doc in docs for word in doc))  # 문서 내 단어의 총 개수 
        self.setlist = list(set(word for doc in docs for word in doc))
        self.K = K  # 토픽 수 
        self.S = S  # 감정수 (예: 긍정, 부정, 중립)

        # Paradigm Word List 
        self.paradigm_pos = paradigm_pos # 긍정 단어 모음 
        self.paradigm_neg = paradigm_neg # 부정 단어 모음 

        # 하이퍼파라미터 
        self.alpha = alpha   # 클수록 다양한 토픽, 감정이 고르게 분포  (0.5 이상이 큼, 0.1~0.01은 작음)
        self.beta = beta   
        self.gamma = gamma 

        # 반복수 
        self.iterations = iterations

        # 초기 행렬 도출 
        self._initialize_counts()


    def _initialize_counts(self):
        
        self.n_dsk = np.zeros((len(self.docs), self.S, self.K)) # 문서수 by 감정 수 by 토픽 수 
        
        self.n_skw = np.zeros((self.S, self.K, self.V)) # 감정 수 by 토픽 수 by 문자 수 
        
        self.n_sk = np.zeros((self.S, self.K)) # 감정 수  by 토픽 수 
        
        self.n_ds = np.zeros((len(self.docs), self.S)) # 문서수 by 감정 수 

        self.topic_assignments = []  
        self.sentiment_assignments = []  

        # 문서별로 감정과 주제를 초기화
        for d, doc in enumerate(self.docs):
            current_topics = []
            current_sentiments = []
            for i, word in enumerate(doc):
                if word in self.paradigm_pos:
                    s = 0 # 긍정 할당
                elif word in self.paradigm_neg:
                    s = 1 # 부정 할당   
                else:
                    s = np.random.randint(0, self.S)  # paradigm에 속하지 않은 단어에 대해  감정을 랜덤 초기화 할당 
                k = np.random.randint(0, self.K)  # 모든 단어에 대해 주제를 랜덤 초기화 할당 
                current_sentiments.append(s)
                current_topics.append(k)
                w = self.setlist.index(word)

                # 카운트 초기화
                self.n_dsk[d][s][k] += 1
                self.n_skw[s][k][w] += 1
                self.n_sk[s][k] += 1
                self.n_ds[d][s] += 1
         
            self.topic_assignments.append(current_topics) 
            self.sentiment_assignments.append(current_sentiments)
           
    
       
    def _sample(self, d, i):
        current_topic = self.topic_assignments[d][i]
        current_sentiment = self.sentiment_assignments[d][i]
       
        # 기존 값 제거 (감정과 주제 할당을 업데이트하기 전)
        if self.n_dsk[d][current_sentiment][current_topic] > 0:
            self.n_dsk[d][current_sentiment][current_topic] -= 1

        w = self.setlist.index(self.docs[d][i])

        if self.n_skw[current_sentiment][current_topic][w] > 0:
            self.n_skw[current_sentiment][current_topic][w] -= 1
        if self.n_sk[current_sentiment][current_topic] > 0:
            self.n_sk[current_sentiment][current_topic] -= 1
        if self.n_ds[d][current_sentiment] > 0:
            self.n_ds[d][current_sentiment] -= 1

        # 새로운 감정과 주제 샘플링
        probabilities = np.zeros((self.S, self.K))
        for s in range(self.S):
            for k in range(self.K):
                
                # 감정-주제-단어 확률
                left_term = (self.n_skw[s][k][w] + self.beta) / (self.n_sk[s][k] + self.V * self.beta)
                # 문서-감정-주제 확률
                middle_term = (self.n_dsk[d][s][k] + self.alpha) / (self.n_ds[d][s] + self.K * self.alpha)
                # 감정 확률
                right_term = (self.n_ds[d][s] + self.gamma) / (len(self.docs[d]) + self.S * self.gamma)
              
                probabilities[s][k] = left_term * middle_term * right_term  # p(s,k | d,w)
       

        # 확률에 따라 새로운 감정과 주제를 샘플링
        probabilities = probabilities.flatten()
        chosen_idx = np.random.choice(np.arange(len(probabilities)), p=probabilities / probabilities.sum())
        new_sentiment, new_topic = divmod(chosen_idx, self.K)


        # 카운트 업데이트
        self.n_dsk[d][new_sentiment][new_topic] += 1
        self.n_skw[new_sentiment][new_topic][w] += 1
        self.n_sk[new_sentiment][new_topic] += 1
        self.n_ds[d][new_sentiment] += 1

        return new_sentiment, new_topic


    def _compute_distributions(self):
        # 감정-주제-단어 분포
        phi = (self.n_skw + self.beta) / (self.n_sk[:, :, np.newaxis] + self.V * self.beta)
        # 문서-감정-주제 분포 
        theta = (self.n_dsk + self.alpha) / (self.n_ds[:, :, np.newaxis] + self.K * self.alpha)
        # 문서-감정 분포 
        pi = (self.n_ds + self.gamma) / (np.sum(self.n_ds, axis=1)[:, np.newaxis] + self.S * self.gamma)
        return phi, theta, pi, self.setlist


    def run(self):
        for iteration in tqdm.tqdm(range(self.iterations)):
            for d, doc in enumerate(self.docs):
                for i, word in enumerate(doc):
                    new_sentiment, new_topic = self._sample(d, i)
                    self.sentiment_assignments[d][i] = new_sentiment
                    self.topic_assignments[d][i] = new_topic
        return self._compute_distributions()  



# 뉴스 데이터 
news_data = pd.read_csv("C:/Users/user/Desktop/hackton_2024/news_data.csv")

news_data_1week = news_data[news_data['news_date'].str.contains(r'2024\.10\.(1[9]|2[0-5])\.\s오후\s\d{1,2}:\d{2}')]
news_data_2week = news_data[news_data['news_date'].str.contains(r'2024\.10\.(1[2-8])\.\s오후\s\d{1,2}:\d{2}')]
news_data_2week = news_data_2week.dropna()
news_data_2week = news_data_2week.reset_index()
news_data_1week = news_data_1week.reset_index()
news_data_1week = news_data_1week.drop("index",axis=1)


#Kkma로 형태소 분석

!pip install konlpy
from konlpy.tag import Okt
okt = Okt()
news_data_1_week_token = [] 

for iterate in range(len(news_data_1week)):
    n_adj = []
    document_lst = okt.pos(news_data_1week["news_content"][iterate])

    for word, tag in document_lst:
        if tag in ["Noun","Adjective"]:
            n_adj.append(word)
    # 블용어 처리 
    stop_words = " 대한 윤석열 대해 한동훈 대통령 여사 대통령실  명태 올해 관련 대해 위해 최근 여사 김건희 우리 라며 대한 의원 입니다 윤석열 한동훈 대통령 민주당 러시아 대통령실 문재인 명씨 신수지 보이 필요하다 있는 있어 배민 커넥트 배민프모 쿠팡 퀄리 카카오 가 가장 같은 같이 것 것과 것이 것도 게 결론적으로 결과적으로 경우 거의 경향이 고 곳 그 그가 그들 그는 그녀 그들 그때 그래서 그러나 그런 그렇다 그리고 그만큼 그밖에 그에 그에게 그에게서 그에겐 그였고 그중 그중에 그중에서도 극히 근거로 근거한 기에 기타 까지 나 나머지 나아가 나와 나는 날 내 내내 내에서 너희 너희가 너무 내가 너의 더구나 더욱 더군다나 더불어 덕분에 도대체 때문에 또한 때 따라서 띄어쓰기 로 마다 만큼 말하자면 무렵 무슨 뭐 모든 무엇 미만 바 바로 바와 반면에 반해 받아 버린 별 별로 본 부터 뿐만 뿐만이 사이 새롭게 생각에 생각에서 생각하면 서로 설명했듯이 소위 손 수 순간 시 실제로 실제 아 아까 아니 아니다 아닙니다 아래 아무래도 아주 안 앞서 약간 언제 어디 어때 어떤 어떻게 여기 여기에 여전히 역시 여러 여러가지 여러개 여러차례 예를 예를들면 오 오늘 오히려 와 왜 외 요 요즘 우리는 우리의 우리도 우리를 우리를위해 우리는 우리에게 우리에게서 우리도 우리를 우리는 우선 이 이가 이게 이런 이러한 이라고 이란 이로 이를 이른 이와 이외 이후 있다 있으면 있지만 잘 잘못 전 전반적으로 전부 전체 절대 절대로 정말 정말로 정리해 정작 제 제가 제기 제때 제발 조차 좀 좋은 좋지 좋았다 중요하게 중심으로 중요한 중에서 지금 지금까지 지켜야 차례로 참 참으로 첫 처음 처음에는 처음으로 추가적으로 치고 크기 큰 클 통해 통하여 특히 파악하고 하게 하겠다고 하곤 하기에 하고 하기에 하게 하고나서 하나 하나같이 한 한데 한때 한편으로 할 한다 한마디로 할수있다 함께 한편으로 할때 하여 해야 할수 해보았다 해보면 해봤다 해야한다 해야할 하고있고 하고있는 해왔다 했었다 했으며 해왔고 해왔지만 하여 했을때 할지 할때마다 했으며 할때만 하는중에 할때만 했으나 했었고 하여야 할수없었다 하여야할때 하여야할 할수있을 했으며 했을 해오면서 해오기위해 해왔으나 해오려고 하여금 했고 했으나 할수없게 했으나 했지만 하여금 했고 했지만 할수없었다 했지만 할때까지 했을때까지 했지만 할때만 했을때까지 하여야 했다"

    stop_words = set(stop_words.split(' '))
    n_adj = [word for word in n_adj if not word in stop_words and len(word) > 1]
    news_data_1_week_token.append(n_adj)

news_data_2_week_token = [] 
for iterate in range(len(news_data_2week)):
    n_adj = []
    document_lst = okt.pos(news_data_2week["news_content"][iterate])

    for word, tag in document_lst:
        if tag in ["Noun","Adjective"]:
            n_adj.append(word)
    # 블용어 처리 
    stop_words = "대한 윤석열 대해 한동훈 대통령 여사 대통령실  명태 올해 관련 대해 위해 최근 여사 김건희 우리 라며 대한 의원 입니다 윤석열 한동훈 대통령 민주당 러시아 대통령실 명씨 문재인 신수지 보이 필요하다 있는 있어 배민 커넥트 배민프모 쿠팡 퀄리 카카오 가 가장 같은 같이 것 것과 것이 것도 게 결론적으로 결과적으로 경우 거의 경향이 고 곳 그 그가 그들 그는 그녀 그들 그때 그래서 그러나 그런 그렇다 그리고 그만큼 그밖에 그에 그에게 그에게서 그에겐 그였고 그중 그중에 그중에서도 극히 근거로 근거한 기에 기타 까지 나 나머지 나아가 나와 나는 날 내 내내 내에서 너희 너희가 너무 내가 너의 더구나 더욱 더군다나 더불어 덕분에 도대체 때문에 또한 때 따라서 띄어쓰기 로 마다 만큼 말하자면 무렵 무슨 뭐 모든 무엇 미만 바 바로 바와 반면에 반해 받아 버린 별 별로 본 부터 뿐만 뿐만이 사이 새롭게 생각에 생각에서 생각하면 서로 설명했듯이 소위 손 수 순간 시 실제로 실제 아 아까 아니 아니다 아닙니다 아래 아무래도 아주 안 앞서 약간 언제 어디 어때 어떤 어떻게 여기 여기에 여전히 역시 여러 여러가지 여러개 여러차례 예를 예를들면 오 오늘 오히려 와 왜 외 요 요즘 우리는 우리의 우리도 우리를 우리를위해 우리는 우리에게 우리에게서 우리도 우리를 우리는 우선 이 이가 이게 이런 이러한 이라고 이란 이로 이를 이른 이와 이외 이후 있다 있으면 있지만 잘 잘못 전 전반적으로 전부 전체 절대 절대로 정말 정말로 정리해 정작 제 제가 제기 제때 제발 조차 좀 좋은 좋지 좋았다 중요하게 중심으로 중요한 중에서 지금 지금까지 지켜야 차례로 참 참으로 첫 처음 처음에는 처음으로 추가적으로 치고 크기 큰 클 통해 통하여 특히 파악하고 하게 하겠다고 하곤 하기에 하고 하기에 하게 하고나서 하나 하나같이 한 한데 한때 한편으로 할 한다 한마디로 할수있다 함께 한편으로 할때 하여 해야 할수 해보았다 해보면 해봤다 해야한다 해야할 하고있고 하고있는 해왔다 했었다 했으며 해왔고 해왔지만 하여 했을때 할지 할때마다 했으며 할때만 하는중에 할때만 했으나 했었고 하여야 할수없었다 하여야할때 하여야할 할수있을 했으며 했을 해오면서 해오기위해 해왔으나 해오려고 하여금 했고 했으나 할수없게 했으나 했지만 하여금 했고 했지만 할수없었다 했지만 할때까지 했을때까지 했지만 할때만 했을때까지 하여야 했다"
    stop_words = set(stop_words.split(' '))
    n_adj = [word for word in n_adj if not word in stop_words and len(word) > 1]
    news_data_2_week_token.append(n_adj)


# 토큰화 

!pip install gensim
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess

stem_lst = news_data_1_week_token + news_data_2_week_token

# Dictionary 객체 생성 (단어-숫자 매핑)
dictionary = Dictionary(stem_lst)

# 각 문장을 숫자 ID로만 변환
news_data_1_week_vector = [dictionary.doc2idx(text) for text in news_data_1_week_token]
news_data_2_week_vector = [dictionary.doc2idx(text) for text in news_data_2_week_token]

# 추가 불용어 처리 

stop_words = dictionary.doc2idx(["즈음", "있었느냐", "좋겠고","김석기", "도의", "즈음", "범여사","부산","박정희", "국정감사", "수수료","댓글","글","더","입니다","배","봇","클린","등록","보기","게시","멤버", "유신고", "개", "있는", "그럼", "가면", "강북", "깡남", "진짜","합","밥","겜","나가야","저","구원","만","시티","건","거","츠","요기","답","도","있습니다","있는","때문","료","또","플러스","님","해","후","등","걸","점","기요","번","알","율","업","중","듯","은","월","민","못","울트라","자","함","쪽","맘","키","임","줄","데","기","놈","식","그냥","고센","가입","정도","유","포","형","비","재","주","네이버","쿠","어제","조대","피","추석","이즈","처","리","명","위","애","복","팡","와우","아프니까","용","분","이제","명절","말","난","강남","여자","남","투표","술","민아","눈","땐","친구","장","살","서울","너","니","누나","남자","씨","피자","아들","학원","우리","봄","여름","인대","한잔","그게","속","분위기","응", "바람","같은데", "다리", "얼굴", "방","형님", "겨울", "온", "여행", "결혼", "바람", "뉴스", "혼자", "마트", "센터", "연휴", "내일", "안주","깜미", "주말", "안주", "혹시", "안녕하세요","달", "가야", "담배", "보고","머","문","발", "바닥", "외국인", "가족", "작년","한국","물", "디", "모두", "박스","전자" ,"탑", "가요", "통", "건가", "아니면", "워드", "기존", "카메라", "블랙박스", "젠", "매일","주간", "생각", "카페","및","신분","있는데", "안타", "가즈", "낮", "여", "라무", "미", "횽들" ,"흠", "왜케","만두","금제","개통","유심","헬로모바일", "쥬", "가을", "밤", "같아요", "애기", "떡볶이","맛집", "당신" ,"편", "오빠", "죽", "기본","로또", "옷","대치동","치킨","없나","고기","탕","국내","빵", "마라","노래","국가", "세대","라이", "아버지","누가", "미래", "새우","왕십리", "민족", "국물", "딸", "습", "노","인","끼", "나라", "마넌", "즉", "무", "이번", "횽", "유재석", "탐라", "도야지", "유부", "갈비탕", "가나", "반포", "가슴", "돌이", "홈런","쇼", "검은","허리","에어컨","주식", "절", "던데", "다가", "행", "햄버거","낼","아내","미국", "해도","묵은지", "토핑", "와이프", "계신가요", "넹", "타고", "이사", "그래", "엄마", "두", "열", "외국", "있던","산","과","레이", "어차피", "수원", "제목", "하하", "이모티콘", "아시", "자영", "입니다","안녕하세요", "답", "글쓰기", "글", "클린", "봇", "유신고", "멤버", "악성", "요기", "와우", "게시", "님", "개", "저", "비", "배", "클럽", "츠", "아빠", "장님", "저희", "프로", "강서구"])
news_data_1_week_token = [[word for word in sublist if word not in stop_words] for sublist in news_data_1_week_token]
news_data_2_week_token= [[word for word in sublist if word not in stop_words] for sublist in news_data_2_week_token]


# 토큰화 
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess

stem_lst = news_data_1_week_token + news_data_2_week_token

# Dictionary 객체 생성 (단어-숫자 매핑)
dictionary = Dictionary(stem_lst)

# 각 문장을 숫자 ID로만 변환
news_data_1_week_vector = [dictionary.doc2idx(text) for text in news_data_1_week_token]
news_data_2_week_vector = [dictionary.doc2idx(text) for text in news_data_2_week_token]


# 사전 정보 
vocab_list = dictionary.token2id
negative = dictionary.doc2idx(["논란","문제","의혹","탄핵","논란","손상","조롱","고의", "박정희", "국정감사", "수수료","북한", "전단","살포","소음","대남", "우크라이나", "전쟁", "참사", "세월호", "악성","아닌데","안되는", "부담","욕","부적절한","지연","스트레스","고생","손해","피해","사고","불가","힘드네요","안됨","진상","짜증","아프다","적자","안됩니다","안된다고","힘든", "비싸게", "비싼","나쁜", "망해라", "어려운", "이상한", "아픈", "죄송합니다", "바쁜", "안되는데", "아니죠", "안된다","힘들어요","아프니","힘들고", "안되니","싫어서","힘들","안될","안되", "답답하네요","어렵네요", "힘들어", "안되죠", "안된", "안좋은","아퍼","이상하게","힘들게","바빠서","안되는거","아파요", "힘듭니다","싫으면", "힘들다","싫고","힘든데","심하네요","답답합니다","힘들어서","죄송하다고","죄송하다","심각하네요","아프네요","힘들어도", "비싸요", "너무하네요", "비싸다고","비싸고", "망하는","싫어요","어렵습니다","답답해서","짜증나서", "심각한", "힘들다고","망할", "무섭네요","싫은", "힘들죠","안된다는","부족한","죄송하지만","심합니다","이상하네요", "거절","똥콜","고생", "콜사", "따리", "할증", "위반", "신고", "문제", "취소", "불법", "금지", "포기", "없고", "실패", "퇴각", "이상",  "고민", "퇴각", "먼", "폭발", "최악", "민원"])
positive = dictionary.doc2idx(["한강","코리아","하니","채식주의자","노벨문학상","뉴진스","좋아요","가능합니다","열정","화이팅","대박","행복","정상","좋겠네요","편하게","가까운", "좋아", "행복한", "좋습니다", "괜찮은","좋은데", "좋네요","좋을","좋게", "우아한", "좋고", "그렇죠","공정한", "착한","맛있게","좋다고","좋죠","다행히","좋아서", "좋을듯", "아름다운", "좋다","친절하게","고맙습니다","맛있는", "소중한","쉬운","즐거운","편해요","편합니다", "괜찮아요","좋아하는","대단한", "달콤한", "친절한","퇴근", "추천", "완료", "피크", "화이팅" , "꿀콜", "무복", "혜택"])
paradigm_pos = positive # 각 긍정 및 부정 단어도 토큰화 수행 
paradigm_neg = negative

# 하이퍼 파라미터 알파, 베타, 감마는 클수록 다양한 토픽, 감정이 고르게 분포  (0.5 이상이 큼, 0.1~0.01은 작음)
# K : 토픽 수, S : 감정 수 
jst = JST(docs=news_data_1_week_vector, K=11, S = 2, alpha=0.5, beta=0.5, gamma= 0.5, iterations=50, paradigm_pos = paradigm_pos,  paradigm_neg= paradigm_neg)   
phi, theta, pi, set_list = jst.run()


# 토큰과 매핑되는 단어 찾기 
word_lst = [] 
for i in set_list:    
    word_lst.append( dictionary[i] )


second_week_topic1 = []

indexed_list = list(enumerate(phi[0][12])) # 긍정 : 0 

# 값에 따라 내림차순으로 정렬
sorted_indexed_list = sorted(indexed_list, key=lambda x: x[1], reverse=True)

# 상위 30개의 값과 인덱스를 추출
top_20_with_index = sorted_indexed_list[:30]

for index, value in top_20_with_index:
    second_week_topic1.append(word_lst[index])
    print(f"Index: {index}, Word: {word_lst[index]}, Value: {value}")


first_week_topic = pd.DataFrame({
    "second_week_topic_topic1": pd.Series(second_week_topic1),
    "second_week_topic2": pd.Series(second_week_topic2),
    "second_week_topic5": pd.Series(second_week_topic5),
    "second_week_topic8": pd.Series(second_week_topic8),
    "second_week_topic9": pd.Series(second_week_topic9),
    "second_week_topic10": pd.Series(second_week_topic10)})



jst = JST(docs=news_data_1_week_vector, K=13, S = 2, alpha=0.5, beta=0.5, gamma= 0.5, iterations=50, paradigm_pos = paradigm_pos,  paradigm_neg= paradigm_neg)   
phi, theta, pi, set_list = jst.run()



second_week_topic = pd.DataFrame({
    "second_week_topic_topic1": pd.Series(second_week_topic1),
    "second_week_topic2": pd.Series(second_week_topic2),
    "second_week_topic3": pd.Series(second_week_topic3),
    "second_week_topic5": pd.Series(second_week_topic5),
    "second_week_topic7": pd.Series(second_week_topic7),
    "second_week_topic10": pd.Series(second_week_topic10), 
    "second_week_topic13": pd.Series(second_week_topic13)})
   
