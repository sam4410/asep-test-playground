   __tablename__ = 'users'
   id = Column(Integer, primary_key=True, index=True)
   clerk_user_id = Column(String, unique=True, index=True)  # Unique identifier for Clerk user
   __tablename__ = 'invoices'
   id = Column(Integer, primary_key=True, index=True)
   user_id = Column(Integer, index=True)  # Foreign key to User
   client_name = Column(String, index=True)
   amount = Column(Integer)
   status = Column(String)  # 'paid' or 'unpaid' status