module PixelatedService
  module SecurityCasingExamples
    module Key
      VALID_U_U = SecurityCasing::Key.new("295C746984AF7F0C", "698E2885C1DE74E32CD503AD295C746984AF7F0C", ["Ola Bini <ola@bini.ec>",
                                                                                                           "Ola Bini <ola@olabini.se>"], ["1905060826932239808", "3264050876889579764"], :valid, 4096, :RSA, :ultimate, :ultimate)

      EXPIRED_UN_UN = SecurityCasing::Key.new("05A63421F637E333", "41EA1D94F26186026CD4B2B505A63421F637E333", ["Rylee Elise Fowler <rylee@rylee.me>",
                                                                                                               "Rylee Fowler (gmail mail, generally unused) <gando.depth@gmail.com>"], [], :expired, 2048, :RSA, :unknown, :unknown)

      REVOKED_F_UN = SecurityCasing::Key.new("11044FD19FC527CC", "E64F19EBBBE86AA97AF36FD511044FD19FC527CC", ["Michael Rogers <michael@briarproject.org>"], [], :revoked, 2048, :RSA, :full, :unknown)

      EXPIRED_NO_TRUST = SecurityCasing::Key.new("FB3973E142A913A4", "AB465EE7022B68C42DBAD324FB3973E142A913A4", ["Michael Granger <ged@FaerieMUD.org>", "Michael Granger <mgranger@rmd.net>", "Michael Granger <mgranger@wwwa.com>",
                                                                                                                  "Michael Granger <rubymage@gmail.com>", "Ged the Grey's Hain <ged@FaerieMUD.org>",
                                                                                                                  "Michael Granger <devEiant@devEiate.org>", "Michael Granger <mgranger@800-all-news.com>",
                                                                                                                  "Michael Granger <mgranger@rubycrafters.com>", "Michael Granger (at work) <mgranger@laika.com>"],
                                                 [], :expired, 1024, :DSA, :no_trust, :no_trust)

      VALID_NO_TRUST = SecurityCasing::Key.new("29F16F77D77A211F", "692B652B70BC67E8EEA36E0929F16F77D77A211F", ["Christian Trabold <info@christian-trabold.de>",
                                                                                                                "Christian Trabold <christian.trabold@dkd.de>"], [], :valid, 4096, :RSA, :no_trust, :no_trust)

      EXAMPLES = [
                  VALID_U_U,
                  SecurityCasing::Key.new("37561129CF4BE610", "D37F700C25569B6F1E1286EF37561129CF4BE610", ["Molly <mollyslop@37dias.com>"], [], :valid, 4096, :RSA, :ultimate, :no_trust),
                  EXPIRED_UN_UN,
                  EXPIRED_NO_TRUST,
                  SecurityCasing::Key.new("E62030AB4AA41495", "BEB9D9E74B0C5167C5FC6CC8E62030AB4AA41495", ["Christopher Dell <chris@tigrish.com>"], ["4117763089493997091"], :valid, 2048, :RSA, :unknown, :full),
                  SecurityCasing::Key.new("D692003DAA02C70A", "3E053E70DE40B13ADE913E7ED692003DAA02C70A", ["Tyler Hicks <tyhicks@tyhicks.net>", "Tyler Hicks <tyhicks@ou.edu>", "Tyler Hicks <tyhicks@gmail.com>",
                                                                                                           "Tyler Hicks <tyhicks@kernel.org>", "Tyler Hicks <tyhicks@ubuntu.com>", "Tyler Hicks <tyhicks@canonical.com>",
                                                                                                           "Tyler Hicks <tyler.hicks@ubuntu.com>", "Tyler Hicks <tyler.hicks@canonical.com>"],
                                          ["792826280999687388"], :valid, 4096, :RSA, :marginal, :full),
                  REVOKED_F_UN,
                  VALID_NO_TRUST,
                  SecurityCasing::Key.new("5DFEA1062EA46E4F", "14D07803BFF6EFA099988C4B5DFEA1062EA46E4F", ["Henri Salo <henri@nerv.fi>", "Henri Salo <fgeek@kapsi.fi>", "Henri Salo <henri.salo@kapsi.fi>",
                                                                                                           "Henri Salo <henri.salo@qentinel.com>"], [], :valid, 1024, :DSA, :no_trust, :ultimate),
                  SecurityCasing::Key.new("C44FBF8A41A80850", "EE6497E3FEC3773BAD33062DC44FBF8A41A80850", ["Seeta Gangadharan <gangadharan@opentechinstitute.org>"], [], :valid, 2048, :RSA, :marginal, :full),
                  SecurityCasing::Key.new("7934ED27275BDB05", "9A6D46E5E7489C60A1DEFDCA7934ED27275BDB05", ["Ernesto Medina Delgado <edelgado@thoughtworks.com>"], ["2618860400823413108"], :valid, 4096, :RSA, :full, :unknown),
                  SecurityCasing::Key.new("EC73D77206A7B07F", "728CFCA32AAFF261DE88971CEC73D77206A7B07F", ["Aaron Bedra <aaron@thinkrelevance.com>"], ["1494195372012211732"], :revoked, 1024, :DSA, :ultimate, :ultimate),
                  SecurityCasing::Key.new("ACD5E501207FBB0E", "281C60C3D20A19C7D2608302ACD5E501207FBB0E", ["Chip Collier <photex@gmail.com>"], [], :valid, 2048, :RSA, :full, :ultimate),
                  SecurityCasing::Key.new("2ECDE8FDF22DB236", "E6D4C474A259113A02E8F2772ECDE8FDF22DB236", ["Hiroshi Nakamura (NaHi) <nahi@ruby-lang.org>", "Hiroshi Nakamura (NaHi) <nahi@ctor.org>",
                                                                                                           "Hiroshi Nakamura (NaHi) <nakahiro@gmail.com>"], [], :revoked, 2048, :RSA, :no_trust, :marginal),
                  SecurityCasing::Key.new("482ECB2BDAAC67D2", "A00620D62EA9B36A3BB71BDE482ECB2BDAAC67D2", ["severino <irregulator@riseup.net>"], ["2361077248315571916"], :valid, 4096, :RSA, :full, :no_trust),
                 ]

    end

    module Imprint
      VALID        = SecurityCasing::Imprint.new(Key::VALID_U_U, Time.now - 200_123, :SHA256, :valid)
      INVALID      = SecurityCasing::Imprint.new(Key::VALID_U_U, Time.now - 123_345, :SHA256, :invalid)
      NO_MATCH     = SecurityCasing::Imprint.new(nil, Time.now - 42_134, :SHA128, :no_match)
      FROM_EXPIRED = SecurityCasing::Imprint.new(Key::EXPIRED_UN_UN, Time.now - 1_002_123, :SHA128, :from_expired)
      FROM_REVOKED = SecurityCasing::Imprint.new(Key::REVOKED_F_UN, Time.now - 12_123, :SHA128, :from_revoked)
      VALID_FROM_NO_TRUST = SecurityCasing::Imprint.new(Key::VALID_NO_TRUST, Time.now - 10_424, :SHA512, :valid)

      EXAMPLES = [
                  VALID,
                  INVALID,
                  NO_MATCH,
                  FROM_EXPIRED,
                  FROM_REVOKED,
                  VALID_FROM_NO_TRUST
                 ]
    end

    module Lock
      VALID_TO_SPECIFIC = SecurityCasing::Lock.new(Key::VALID_U_U, :valid, :RSA, true)
      VALID_NOT_TO_SPECIFIC = SecurityCasing::Lock.new(Key::VALID_U_U, :valid, :RSA, false)

      INVALID_TO_SPECIFIC = SecurityCasing::Lock.new(Key::VALID_U_U, :failure, :RSA, true)
      INVALID_NOT_TO_SPECIFIC = SecurityCasing::Lock.new(Key::VALID_U_U, :failure, :RSA, false)

      EXPIRED_TO_SPECIFIC = SecurityCasing::Lock.new(Key::EXPIRED_UN_UN, :failure, :RSA, true)
      EXPIRED_NOT_TO_SPECIFIC = SecurityCasing::Lock.new(Key::EXPIRED_UN_UN, :failure, :RSA, false)

      REVOKED_TO_SPECIFIC = SecurityCasing::Lock.new(Key::REVOKED_F_UN, :failure, :RSA, true)
      REVOKED_NOT_TO_SPECIFIC = SecurityCasing::Lock.new(Key::REVOKED_F_UN, :failure, :RSA, false)

      NO_KEY_TO_SPECIFIC = SecurityCasing::Lock.new(nil, :no_private_key, :RSA, true)
      NO_KEY_NOT_TO_SPECIFIC = SecurityCasing::Lock.new(nil, :no_private_key, :RSA, false)

      EXAMPLES = [
                  VALID_TO_SPECIFIC,
                  VALID_NOT_TO_SPECIFIC,
                  INVALID_TO_SPECIFIC,
                  INVALID_NOT_TO_SPECIFIC,
                  EXPIRED_TO_SPECIFIC,
                  EXPIRED_NOT_TO_SPECIFIC,
                  REVOKED_TO_SPECIFIC,
                  REVOKED_NOT_TO_SPECIFIC,
                  NO_KEY_TO_SPECIFIC,
                  NO_KEY_NOT_TO_SPECIFIC
                 ]
    end

    module Case
      NO_IMPRINTS_OR_LOCKS = SecurityCasing.new([], [])

      ONE_VALID_IMPRINT = SecurityCasing.new([Imprint::VALID], [])
      THREE_VALID_IMPRINTS = SecurityCasing.new([Imprint::VALID,
                                                 Imprint::VALID,
                                                 Imprint::VALID], [])
      ONE_VALID_TWO_NO_MATCH_IMPRINTS = SecurityCasing.new([Imprint::NO_MATCH,
                                                            Imprint::VALID,
                                                            Imprint::NO_MATCH], [])
      ONE_INVALID_IMPRINT = SecurityCasing.new([Imprint::INVALID], [])
      ONE_NO_MATCH_IMPRINT = SecurityCasing.new([Imprint::NO_MATCH], [])
      FROM_EXPIRED_IMPRINT = SecurityCasing.new([Imprint::FROM_EXPIRED], [])
      FROM_REVOKED_IMPRINT = SecurityCasing.new([Imprint::FROM_REVOKED], [])
      FROM_VALID_WITH_NO_TRUST_IMPRINT = SecurityCasing.new([Imprint::VALID_FROM_NO_TRUST], [])

      WITH_IMPRINTS = [ONE_VALID_IMPRINT, THREE_VALID_IMPRINTS, ONE_VALID_TWO_NO_MATCH_IMPRINTS, ONE_INVALID_IMPRINT, ONE_NO_MATCH_IMPRINT, FROM_EXPIRED_IMPRINT, FROM_REVOKED_IMPRINT, FROM_VALID_WITH_NO_TRUST_IMPRINT]

      VALID_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::VALID_TO_SPECIFIC])
      VALID_NOT_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::VALID_NOT_TO_SPECIFIC])
      ONE_VALID_TWO_INVALID_LOCKS = SecurityCasing.new([], [Lock::VALID_TO_SPECIFIC, Lock::INVALID_TO_SPECIFIC, Lock::INVALID_NOT_TO_SPECIFIC])
      ONE_VALID_TWO_NO_KEY_LOCKS = SecurityCasing.new([], [Lock::NO_KEY_TO_SPECIFIC, Lock::VALID_TO_SPECIFIC, Lock::NO_KEY_NOT_TO_SPECIFIC])
      INVALID_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::INVALID_TO_SPECIFIC])
      INVALID_NOT_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::INVALID_NOT_TO_SPECIFIC])
      EXPIRED_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::EXPIRED_TO_SPECIFIC])
      EXPIRED_NOT_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::EXPIRED_NOT_TO_SPECIFIC])
      REVOKED_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::REVOKED_TO_SPECIFIC])
      REVOKED_NOT_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::REVOKED_NOT_TO_SPECIFIC])
      NO_KEY_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::NO_KEY_TO_SPECIFIC])
      NO_KEY_NOT_TO_SPECIFIC_LOCK = SecurityCasing.new([], [Lock::NO_KEY_NOT_TO_SPECIFIC])

      WITH_LOCKS = [VALID_TO_SPECIFIC_LOCK, VALID_NOT_TO_SPECIFIC_LOCK, ONE_VALID_TWO_INVALID_LOCKS, ONE_VALID_TWO_NO_KEY_LOCKS, INVALID_TO_SPECIFIC_LOCK, INVALID_NOT_TO_SPECIFIC_LOCK,
                    EXPIRED_TO_SPECIFIC_LOCK, EXPIRED_NOT_TO_SPECIFIC_LOCK, REVOKED_TO_SPECIFIC_LOCK, REVOKED_NOT_TO_SPECIFIC_LOCK, NO_KEY_TO_SPECIFIC_LOCK, NO_KEY_NOT_TO_SPECIFIC_LOCK]

      WITH_IMPRINTS_AND_LOCKS = WITH_IMPRINTS.product(WITH_LOCKS).map { |l, r| l + r }

      EXAMPLES = [NO_IMPRINTS_OR_LOCKS] +
        WITH_IMPRINTS +
        WITH_LOCKS +
        WITH_IMPRINTS_AND_LOCKS

      class << self
        def case_from(ident)
          EXAMPLES[ident % EXAMPLES.size]
        end
      end
    end
  end
end
