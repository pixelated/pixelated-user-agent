
fixture1 = File.read(File.join(File.dirname(__FILE__), "..", "fixtures", "mail1"))
fixture2 = File.read(File.join(File.dirname(__FILE__), "..", "fixtures", "mail2"))

describe PixelatedService::Mail do
  describe "#read" do
    context("simple email") do
      subject(:mail) { PixelatedService::Mail.read(fixture1) }

      it "reads the subject correctly" do
        expect(mail.subject).to eq("Doloremque aliquid a facilis et sit numquam libero.")
      end

      it "reads the from correctly" do
        expect(mail.from).to eq("kenneth@willmsmckenzie.org")
      end

      it "reads the to correctly" do
        expect(mail.to).to eq("antonio@beier.biz")
      end

      it "reads and parses date" do
        expect(mail.headers[:date]).to eq(DateTime.parse("2014-05-29T18:56:41 -0300"))
      end

      it "reads the body correctly" do
        expect(mail.body).to eq(<<BODY)
Quia tempora quas laboriosam. Dolorem dolor fuga a aut minima sint. Ullam suscipit consectetur nihil. Incidunt velit aut reprehenderit.

Laborum blanditiis praesentium soluta dolorem laudantium a. Molestiae excepturi laudantium at eos velit. Commodi quaerat suscipit laudantium sapiente aut omnis. Qui iure impedit ea dolores. Et debitis non est tempora id autem.

Atque officia architecto sed assumenda. Inventore quia minus. Doloribus amet reiciendis ipsam aut.
BODY
      end

      it "reads a multi line header correctly" do
        expect(mail.headers[:content_type]).to eq("text/plain; charset=UTF-8")
      end
    end

    context("with multiple recipients") do
      subject(:mail) { PixelatedService::Mail.read(fixture2) }

      it "reads multiple recipients correctly" do
        expect(mail.to).to eq(%w(cmurphy@thoughtworks.com cgorslin@thoughtworks.com cmitchel@thoughtworks.com dnorth@thoughtworks.com dpgoodwi@thoughtworks.com dbodart@thoughtworks.com dsmith@thoughtworks.com djrice@thoughtworks.com dwhalley@thoughtworks.com))
      end

      it "reads multiple cc recipients correctly" do
        expect(mail.headers[:cc]).to eq(%w(amonago@thoughtworks.com agore@thoughtworks.com bswamina@thoughtworks.com baphipps@thoughtworks.com bbutler@thoughtworks.com cwathing@thoughtworks.com))
      end
    end
  end

  describe ".to_s" do
    context("simple email") do
      subject(:mail) { PixelatedService::Mail.read(fixture1) }

      it "writes correct output" do
        expect(mail.to_s).to eq(<<MAIL)
Content-Transfer-Encoding: 7bit
Content-Type: text/plain; charset=UTF-8
Date: Thu, 29 May 2014 18:56:41 -0300
From: kenneth@willmsmckenzie.org
Message-ID: <5387ad199161e_6ced7c32ec77517@norepinephrine.mail>
Mime-Version: 1.0
Subject: Doloremque aliquid a facilis et sit numquam libero.
To: antonio@beier.biz
X-TW-SMail-Ident: 

Quia tempora quas laboriosam. Dolorem dolor fuga a aut minima sint. Ullam suscipit consectetur nihil. Incidunt velit aut reprehenderit.

Laborum blanditiis praesentium soluta dolorem laudantium a. Molestiae excepturi laudantium at eos velit. Commodi quaerat suscipit laudantium sapiente aut omnis. Qui iure impedit ea dolores. Et debitis non est tempora id autem.

Atque officia architecto sed assumenda. Inventore quia minus. Doloribus amet reiciendis ipsam aut.
MAIL
      end
    end
    context("with multiple recipients") do
      subject(:mail) { PixelatedService::Mail.read(fixture2) }

      it "writes correct output" do
        expect(mail.to_s).to eq(<<MAIL)
CC: amonago@thoughtworks.com, agore@thoughtworks.com, bswamina@thoughtworks.com, baphipps@thoughtworks.com, bbutler@thoughtworks.com, cwathing@thoughtworks.com
Content-Transfer-Encoding: 7bit
Content-Type: text/plain; charset=UTF-8
Date: Thu, 29 May 2014 18:56:41 -0300
From: kenneth@willmsmckenzie.org
Message-ID: <5387ad199161e_6ced7c32ec77517@norepinephrine.mail>
Mime-Version: 1.0
Subject: Doloremque aliquid a facilis et sit numquam libero.
To: cmurphy@thoughtworks.com, cgorslin@thoughtworks.com, cmitchel@thoughtworks.com, dnorth@thoughtworks.com, dpgoodwi@thoughtworks.com, dbodart@thoughtworks.com, dsmith@thoughtworks.com, djrice@thoughtworks.com, dwhalley@thoughtworks.com
X-TW-SMail-Ident: 

Quia tempora quas laboriosam. Dolorem dolor fuga a aut minima sint. Ullam suscipit consectetur nihil. Incidunt velit aut reprehenderit.

Laborum blanditiis praesentium soluta dolorem laudantium a. Molestiae excepturi laudantium at eos velit. Commodi quaerat suscipit laudantium sapiente aut omnis. Qui iure impedit ea dolores. Et debitis non est tempora id autem.

Atque officia architecto sed assumenda. Inventore quia minus. Doloribus amet reiciendis ipsam aut.
MAIL
      end
    end
  end
end
