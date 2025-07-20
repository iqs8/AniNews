import os
def generate_html():
  # file_path = os.path.join(os.path.dirname(__file__), 'scraped_content.txt')
  file_path = '/tmp/scraped_content.txt'
  with open(file_path, 'r', encoding='utf-8') as f:

      date_line = f.readline().strip()  # This will be 'Date: ...'
      # Optionally, skip the next blank line if present
      next_line = f.readline()
      newsletter_content = f.read()  # The rest of the file

  date = date_line.replace('Date: ', '')



  message = """You are making a newsletter for the AniNews Newsletter. It's your job to receive yesterday's anime news and summarize 
  it into a daiy newsletter. Start the newsletter with a greeting (mentioning that this newsletter is for yesterday's news), 
  and sign off as AniNews ai. Do not include a subject. 
  Your only output should be the email which will be sent directly to readers. 

  Your response must be a complete HTML document using inline CSS and the exact layout below. Do not include any markdown or explanations. 
  Your only output should be the raw HTML. Do not modify the unsub link, keep it exactly as is.

  Group stories under the following exact categories and emoji-labeled headers. Only include categories that contain at least one story:

  ✨ Anime and Live-Action
  📖 Manga & Publishing
  🎮 Game News
  📰 Industry & Extras

  MAKE SURE TO INCLUDE ALL STOIRES. The html below is just an example. 
  
  Use the following HTML structure as a template. Replace the content with real stories, maintaining the format, styling, and grouping — do not create empty headers.

  ---

  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="UTF-8">
    <title>Anime-GPT Newsletter</title>
    <style>
      body {
        margin: 0;
        background-color: #fffdfd;
        font-family: 'Georgia', serif;
        color: #333;
      }
      .container {
        max-width: 700px;
        margin: 40px auto;
        background: #ffffff;
        padding: 30px;
        border-radius: 12px;
        border: 1.5px solid #dab6f9;
        box-shadow:
          0 0 5px rgba(245, 133, 186, 0.15),
          0 0 10px rgba(186, 119, 255, 0.08);
      }
      h1 {
        text-align: center;
        font-size: 28px;
        color: #854edb;
        margin-bottom: 12px;
      }
      .subtitle {
        text-align: center;
        font-size: 15px;
        color: #666;
        margin-bottom: 25px;
      }
      h2 {
        font-size: 18px;
        color: #e754a3;
        border-bottom: 2px dotted #f7bbdf;
        padding-bottom: 5px;
        margin-top: 30px;
      }
      ul {
        padding-left: 1.2em;
      }
      li {
        font-size: 15px;
        margin-bottom: 12px;
        line-height: 1.6;
      }
      strong {
        color: #111;
      }
      .footer {
        margin-top: 40px;
        text-align: center;
        font-style: italic;
        color: #666;
        font-size: 14px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>AniNews Daily Newsletter  </h1>
      <p class="subtitle">Welcome to your daily dose of the latest anime news!</p>

      <h2>✨ Anime and Live-Action</h2>
      <ul>
        <li>
          <strong>Chihayafuru Live-Action Sequel</strong>: The trailer for the upcoming live-action series has dropped, revealing the premiere date on July 9 at 10:00 p.m. on NTV. Set a decade after the original films, the series follows high school students passionate about competitive karuta. The production involves original manga creator Yuki Suetsugu and returning director Norihiro Koizumi.
        </li>
        <li>
          <strong>"10 Things I Want to Do Before I Turn 40"</strong>: TV Tokyo's new live-action boys-love adaptation premieres on July 4. The story centers on Suzume, a man approaching his 40th birthday, and his energetic junior Keishi as they explore unfulfilled dreams and unexpected connection.
        </li>
      </ul>

      <h2>🎮 Game News</h2>
      <ul>
        <li>
          <strong>Shinobi: Art of Vengeance</strong>: Sega unveiled a new trailer for this stylized ninja action game launching August 29 on PS5, Xbox Series X|S, PS4, Switch, and Steam. Players control Joe Musashi in a hand-drawn world, featuring multi-path levels and deep combat.
        </li>
        <li>
          <strong>Elden Ring: Nightreign</strong>: Bandai Namco announced this standalone multiplayer RPG set in the Elden Ring universe, launching May 30. Players explore shifting worlds, battle the Nightlord, and uncover the mystery of the Nightfarer.
        </li>
      </ul>

      <div class="footer">
        That’s all for today! Stay tuned for more anime news tomorrow. 
        <br>Feel free to reply to this email with any feedback you have<br><br>
        Warm regards,<br>
        <strong>AniNews ai</strong>
      </div>

      <div class="unsub" style="margin-top: 25px; padding-top: 20px; border-top: 1px dotted #f7bbdf; font-size: 13px; color: #888; text-align: center;">
          If you no longer wish to receive these emails, you can 
          <a href="{{UNSUB_LINK}}" style="color: #e754a3; text-decoration: underline; font-weight: bold;">
              click here to unsubscribe
          </a>.
      </div>


    </div>
  </body>
  </html>
  ---

  Only output the HTML above with the actual stories and categories inserted. 
  Do not include any explanation or markdown outside the HTML. This will be used as a raw email body.
  Do not wrap the HTML in backticks. Return only the raw HTML without ```html or any markdown formatting.
  """
  from openai import OpenAI
  key = os.environ.get('OPENAI_KEY')
  client = OpenAI(
      api_key=key
  )

  completion = client.chat.completions.create(
    # model="gpt-4.1-nano",
    model="gpt-4o-mini",
    messages=[
      {"role": "user", "content": message + newsletter_content}
    ]
  )

  print("HTML GENERATED")
  htmlResponse = completion.choices[0].message.content
  if htmlResponse.strip().startswith("```html"):
        htmlResponse = htmlResponse.strip()[7:].strip()  # remove ```html
  if htmlResponse.strip().endswith("```"):
      htmlResponse = htmlResponse.strip()[:-3].strip()  # remove ```

  return htmlResponse




