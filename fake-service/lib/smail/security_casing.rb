
module Smail
  class SecurityCasing < Struct.new(:imprints, :locks)
    def to_json(*args)
      { imprints: self.imprints, locks: self.locks }.to_json(*args)
    end

    def +(other)
      imprints = self.imprints + other.imprints
      locks = self.locks + other.locks
      SecurityCasing.new(imprints, locks)
    end

    class Key < Struct.new :longid, :fingerprint, :user_ids, :connected_contacts, :state, :size, :algorithm, :trust, :validity
      VALID_STATES = [:valid, :expired, :revoked]
      VALID_TRUST = [:unknown, :no_trust, :marginal, :full, :ultimate]

      def to_json(*args)
        { longid: self.longid,
          fingerprint: self.fingerprint,
          user_ids: self.user_ids,
          connected_contacts: self.connected_contacts,
          state: self.state,
          size: self.size,
          algorithm: self.algorithm,
          trust: self.trust,
          validity: self.validity }.to_json(*args)
      end
    end

    # Signature
    class Imprint < Struct.new :seal, :imprint_timestamp, :algorithm, :state
      VALID_STATES = [:valid, :invalid, :no_match, :from_expired, :from_revoked]

      def to_json(*args)
        { seal: self.seal,
          imprint_timestamp: self.imprint_timestamp,
          algorithm: self.algorithm,
          state: self.state }.to_json(*args)
      end
    end

    # Encryption
    class Lock < Struct.new :key, :state, :algorithm, :key_specified_in_lock
      VALID_STATES = [:valid, :failure, :no_private_key]

      def to_json(*args)
        { state: self.state,
          algorithm: self.algorithm,
          key: self.key,
          key_specified_in_lock: self.key_specified_in_lock }.to_json(*args)
      end
    end
  end
end
