using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Driver;

namespace Jobs.Api
{
    public class JobPostingRecord
    {
        [BsonId, BsonRepresentation(MongoDB.Bson.BsonType.ObjectId)]
        public string Id { get; set; }

        [BsonElement("source_link"), BsonRepresentation(MongoDB.Bson.BsonType.String)]
        public string SourceLink { get; set; }

        [BsonElement("description"), BsonRepresentation(MongoDB.Bson.BsonType.String)]
        public string Description { get; set; }
    }
    
    public class JobPostingsService
    {
        private readonly string _mongoDbConnectionString;
        private readonly string _mongoDatabaseName;
        private readonly string _defaultCollectionName;

        public JobPostingsService(IConfiguration configuration)
        {
            var mongoConfigurations = configuration.GetSection("MongoDb");
            if (mongoConfigurations == null)
            {
                throw new ArgumentNullException(nameof(mongoConfigurations), "MongoDB configurations are not provided.");
            }

            _mongoDbConnectionString = mongoConfigurations.GetValue<string>("ConnectionString");
            _mongoDatabaseName = mongoConfigurations.GetValue<string>("DatabaseName");
            _defaultCollectionName = mongoConfigurations.GetValue<string>("CollectionName");
        }

        public async Task CreateJobPostingAsync(JobPosting jobPosting)
        {
            using var mongoClient = new MongoClient(_mongoDbConnectionString);
            var mongoDatabase = mongoClient.GetDatabase(_mongoDatabaseName);
            var collection = mongoDatabase.GetCollection<JobPostingRecord>(_defaultCollectionName);

            await collection.InsertOneAsync(new JobPostingRecord
            {
                SourceLink = jobPosting.SourceLink,
                Description = jobPosting.Description
            });
        }
    }
}
